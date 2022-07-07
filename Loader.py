import json
import os
import cv2 as cv
import numpy as np
from requests import request


class Loader:

    def __init__(self, file_path, scale):
        self.cap = cv.VideoCapture(file_path)
        if not self.cap.isOpened():
            print("[Error] Failed to read file")

        self.scaled_size = (int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH) * scale),
                            int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT) * scale))
        self.gray_bg = None
        self.mono_bg = np.full(self.scaled_size[::-1], 244, dtype=np.uint8)
        self.last_idx = 0
        self.armory = []
        self.digits = []
        self.mask = []
        self.ret = None

    def fetch_imgs(self):
        if 'images' not in os.listdir():
            os.mkdir('images')
            fd = open("armory.json")
            for i, url in enumerate(json.load(fd)['URL']):
                res = request.get(url)
                img = cv.imdecode(np.frombuffer(
                    res.content, np.unit8), cv.IMREAD_GRAYSCALE)
                cv.imwrite(f'images/{i}.png', img)
            fd.close()

        for n in sorted(os.listdir('images'), key=(
                lambda name: 10 if name == "x.png" else int(name.split('.')[0]))):
            img = cv.imread(f'images/{n}', cv.IMREAD_GRAYSCALE)
            self.armory.append(cv.blur(img, (2, 2)))

        for n in sorted(os.listdir('digits'), key=(
                lambda name: 10 if name == "x.png" else int(name.split('.')[0]))):
            img = cv.imread(f'digits/{n}', cv.IMREAD_UNCHANGED)
            self.digits.append(cv.cvtColor(img, cv.COLOR_RGB2GRAY))
            self.mask.append(img[:, :, 3])

        self.ret = np.empty(len(self.armory), dtype=object)
        self.ret[:] = [(-1, '')]

    def get_bg(self):
        samples = self.cap.get(cv.CAP_PROP_FRAME_COUNT) * \
            np.random.uniform(size=15)
        frames = []
        for i in samples:
            self.cap.set(cv.CAP_PROP_POS_FRAMES, int(i))
            ret, frame = self.cap.read()
            if not ret:
                print("[Warning] Frame lost (background)")
                continue

            frames.append(cv.resize(
                cv.cvtColor(frame, cv.COLOR_RGB2GRAY),
                self.scaled_size, interpolation=cv.INTER_LINEAR))

        self.gray_bg = np.median(frames, axis=0).astype(np.uint8)

    def slice_2_contours(self, gray):
        diff = cv.absdiff(gray, self.gray_bg)
        diff_mono = cv.morphologyEx(cv.absdiff(
            gray, self.mono_bg), cv.MORPH_TOPHAT, None)
        dilated_diff_mono = cv.dilate(diff_mono, None, iterations=(
            lambda h: 4 if h > 800 else (3 if h > 600 else (2 if h > 400 else 1)))(self.scaled_size[1]))
        dilated_diff = cv.dilate(diff, None, iterations=2)

        res = np.minimum(dilated_diff, dilated_diff_mono)
        _, thres = cv.threshold(res, 12, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(
            thres, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        return contours

    def identify(self):
        interval = 0
        while self.cap.isOpened():
            interval += 1

            ret, frame = self.cap.read()
            if not ret:
                print("Done")
                break

            if interval % 6:
                continue

            frame = cv.resize(frame, self.scaled_size,
                              interpolation=cv.INTER_LINEAR)
            gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
            contours = self.slice_2_contours(gray)

            for contour in contours:
                if cv.contourArea(contour) < pow(self.scaled_size[1] * 0.12, 2):
                    continue
                if cv.contourArea(contour) > pow(self.scaled_size[1] * 0.22, 2):
                    continue

                x, y, w, h = cv.boundingRect(contour)
                if h < w * 0.9:
                    continue
                if h > w * 1.1:
                    continue

                # cv.rectangle(frame, (x, y + 2), (x + w + 1, y + h - 2), (0, 255, 0), 2)

                img = frame[y + 2:y + h - 2, x + 2:x + w - 2]
                gray_img = cv.resize(cv.cvtColor(
                    img, cv.COLOR_RGB2GRAY), (128, 128), interpolation=cv.INTER_LINEAR)

                diff_armory_arr = []
                for i, armory in enumerate(self.armory):
                    if i < self.last_idx - 30:
                        diff_armory_arr.append(0)
                        continue

                    res = cv.matchTemplate(
                        gray_img, armory, cv.TM_CCOEFF_NORMED)
                    vmin, vmax, _, _ = cv.minMaxLoc(res)
                    diff_armory_arr.append(vmax)

                    if vmax > 0.76:
                        self.last_idx = i
                        break
                    if i > self.last_idx + 45:
                        break

                matched_armory_idx = np.argmax(diff_armory_arr)

                # if matched_armory_idx == 10:
                #     print(np.amax(diff_armory_arr))

                if np.amax(diff_armory_arr) < 0.74:
                    continue
                if np.amax(diff_armory_arr) < self.ret[matched_armory_idx][0]:
                    continue

                partition = gray_img[100:118, :]
                digit_partition = [partition[:, 109:123], partition[:, 94:108],
                                   partition[:, 79:93], partition[:, 64:78], partition[:, 49:63]]

                solved_digits = []
                for digit in digit_partition:
                    tmp = []
                    for i, d in enumerate(self.digits):
                        res = cv.matchTemplate(
                            digit, d, cv.TM_CCOEFF_NORMED, mask=self.mask[i])
                        _vmin, _vmax, _, _ = cv.minMaxLoc(res)
                        tmp.append(_vmax)

                    # if matched_armory_idx == 10:
                    #     print(tmp)

                    if np.amax(tmp) < 0.65:
                        break

                    matched_digit_idx = np.argmax(tmp)
                    if matched_digit_idx == 10:
                        solved_digits.append('x')
                        break
                    else:
                        solved_digits.append(matched_digit_idx)

                numeric = ''
                solved_digits.reverse()
                if len(solved_digits) != 0 and solved_digits[0] != 'x':
                    continue

                for s in solved_digits:
                    numeric += str(s)

                self.ret[matched_armory_idx] = (
                    np.amax(diff_armory_arr), numeric)

            cv.imshow("preview", frame)
            if cv.waitKey(25) & 0xff == ord('q'):
                break

        fd = open("result.json", 'w')
        json.dump(self.ret.tolist(), fd)
        fd.close()

        self.cap.release()
        cv.destroyAllWindows()

    def run(self):
        self.fetch_imgs()
        self.get_bg()
        self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        self.identify()
