<a id="top"></a>

<!-- Banner -->
<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin" style="border: none;">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology">
  </a>
</p>

<h1 align="center"><b>TRUY VẤN THÔNG TIN ĐA PHƯƠNG TIỆN<br>(MULTIMEDIA INFORMATION RETRIEVAL)</b></h>

[![Status](https://img.shields.io/badge/status-working-pink?style=flat-square)](https://github.com/pahopu/CS336_ImageSearch_Project2)
[![GitHub contributors](https://img.shields.io/github/contributors/pahopu/CS336_ImageSearch_Project2?style=flat-square)](https://github.com/pahopu/CS336_ImageSearch_Project2/graphs/contributors)
[![Status](https://img.shields.io/badge/language-python-blue?style=flat-square)](https://github.com/pahopu/CS336_ImageSearch_Project2)
[![Status](https://img.shields.io/badge/language-html-orange?style=flat-square)](https://github.com/pahopu/CS336_ImageSearch_Project2)
[![Status](https://img.shields.io/badge/language-css-purple?style=flat-square)](https://github.com/pahopu/CS336_ImageSearch_Project2)
[![Status](https://img.shields.io/badge/language-javascript-yellow?style=flat-square)](https://github.com/pahopu/CS336_ImageSearch_Project2)

## [BẢNG MỤC LỤC](#top)
* [Giới thiệu môn học](#giới-thiệu-môn-học)
* [Thông tin các thành viên](#thông-tin-về-các-thành-viên-nhóm)
* [Thông tin đồ án](#thông-tin-đồ-án)
* [Các bước cần thiết](#các-bước-cần-thiết)
* [Chuẩn bị dataset](#chuẩn-bị-dataset)
* [Indexing và Evaluating](#indexing-và-evaluating)
* [Chạy hệ thống trên web](#chạy-hệ-thống-trên-web)
* [Demo video](#demo-video)

## [GIỚI THIỆU MÔN HỌC](#top)
* **Tên môn học:** Truy vấn thông tin đa phương tiện - Multimedia Information Retrieval
* **Mã môn học:** CS336
* **Mã lớp:** CS336.N11.KHCL
* **Năm học:** HK1 (2022 - 2023)
* **Giảng viên:** TS. Ngô Đức Thành

## [THÔNG TIN VỀ CÁC THÀNH VIÊN NHÓM](#top)

| STT    | MSSV          | Họ và Tên                |Vai trò    | Github                                          | Email                   |
| :----: |:-------------:| :-----------------------:|:---------:|:-----------------------------------------------:|:-------------------------:
| 1      | 20520278      | Phạm Hoàng Phúc          |Trưởng nhóm|[pahopu](https://github.com/pahopu)              |20520278@gm.uit.edu.vn   |
| 2      | 20520313      | Nguyễn Hồng Anh Thư      |Thành viên |[thuwpink](https://github.com/thuwpink)          |20520313@gm.uit.edu.vn   |
| 3      | 20521446      | Huỳnh Nguyễn Vân Khánh   |Thành viên |[hnvkhanh](https://github.com/hnvkhanh)          |20521446@gm.uit.edu.vn   |
| 4      | 20521546      | Lê Tấn Lộc               |Thành viên |[leetnlok](https://github.com/leetnlok)          |20521546@gm.uit.edu.vn   |

## [THÔNG TIN ĐỒ ÁN](#top)
* **Tên đồ án:** Hệ thống truy vấn thông tin bằng hình ảnh - Content-Based Information Retrieval System
* **Ngôn ngữ lập trình:** Python, HTML, CSS, JavaScript
* **Input:** Một bức ảnh (có thể crop)
* **Output:** Một tập những bức ảnh được xem là liên quan đến bức ảnh đầu vào

## [CÁC BƯỚC CẦN THIẾT](#top)
Sử dụng Git Bash để có thể khởi chạy project.

### 1. Clone project
Clone project repository bằng câu lệnh dưới đây.

```bash
git clone https://github.com/pahopu/CS336_ImageSearch_Project2.git
```

### 2. Cài đặt thư viện
Cài đặt các thư viện cần thiết cho project với câu lệnh dưới đây.

```bash
cd CS336_ImageSearch_Project2
python3 -m pip install -r requirements.txt
```

## [CHUẨN BỊ DATASET](#top)
* Ở đây, chúng ta có thể sử dụng 2 bộ dataset là Oxford Buildings và Paris Buildings để thực hiện truy vấn.
* Đường dẫn tải dataset và groundtruth sẽ được gắn ở phần chi tiết bên dưới.

### Yêu cầu truy cập
Trước hết, chúng ta phải điền [form](https://docs.google.com/forms/d/e/1FAIpQLSeIWlksO7O2TxeftwR8vzEZ9ivPj29TuB_Zv_9glda9a1_rLQ/viewform) để được cung cấp **tên đăng nhập** và **mật khẩu** để tải các bộ dataset nói trên.

### 1. Oxford Buildings
* Ta tải các ảnh trong dataset Oxford Buildings tại [đây](https://thor.robots.ox.ac.uk/datasets/oxford-buildings/oxbuild_images-v1.tgz).
* Sau đó, giải nén và đặt nó vào trong thư mục ```static/datasets/oxbuild/images```
* Cấu trúc như sau:
  ```
  CS336_ImageSearch_Project2
              └───static
                    └───datasets
                           └───oxbuild
                                  └───images
                                        │all_souls_000000.jpg
                                        │all_souls_000001.jpg
                                        │all_souls_000002.jpg
                                        |all_souls_000003.jpg
                                        |...
  ```

* Ta cũng cần phải tải các file groundtruth tại [đây](https://www.robots.ox.ac.uk/~vgg/data/oxbuildings/gt_files_170407.tgz).
* Giải nén và đặt nó trong thư mục ```static/datasets/oxbuild/groundtruth```
* Cấu trúc như sau:
  ```
  CS336_ImageSearch_Project2
              └───static
                    └───datasets
                           └───oxbuild
                                  └───groundtruth
                                           │all_souls_1_good.txt
                                           │all_souls_1_junk.txt
                                           │all_souls_1_ok.txt
                                           │all_souls_1_query.txt
                                           |...
  ```

### 2. Paris Buildings
* Đối với bộ dataset này, nó được chia ra làm 2 phần. Ta có thể tải tại đây:
   * [paris_part1](https://thor.robots.ox.ac.uk/datasets/paris-buildings/paris_1-v1.tgz)
   * [paris_part2](https://thor.robots.ox.ac.uk/datasets/paris-buildings/paris_2-v1.tgz)
* Sau đó, giải nén cả 2 và đặt chúng cùng vào trong thư mục ```static/datasets/paris/images```
* Cấu trúc như sau:
  ```
  CS336_ImageSearch_Project2
              └───static
                    └───datasets
                           └───paris
                                 └───images
                                       │paris_defense_000000.jpg
                                       │paris_defense_000002.jpg
                                       │paris_defense_000004.jpg
                                       |paris_defense_000005.jpg
                                       |...
  ```

* Ta cũng cần phải tải các file groundtruth tại [đây](https://www.robots.ox.ac.uk/~vgg/data/parisbuildings/paris_120310.tgz).
* Giải nén và đặt nó trong thư mục ```static/datasets/paris/groundtruth```
* Cấu trúc như sau:
  ```
  CS336_ImageSearch_Project2
              └───static
                    └───datasets
                           └───paris
                                 └───groundtruth
                                          │defense_1_good.txt
                                          │defense_1_junk.txt
                                          │defense_1_ok.txt
                                          │defense_1_query.txt
                                          |...
  ```

## [INDEXING VÀ EVALUATING](#top)
* Trong project này, chúng tôi đã cài đặt 6 feature extractors để thử nghiệm. Chúng lần lượt là:
  * VGG16
  * Xception
  * InceptionV3
  * ResNet152V2
  * EfficientNetV2L
  * InceptionResNetV2
* Qua thực nghiệm, chúng tôi thấy rằng phương pháp **Xception** cho kết quả tốt nhất trong thời gian ngắn nhất.
* Chúng ta có thể **indexing** và **evaluating** cho 2 bộ dataset đã nêu trên cho 6 phương pháp này.
* Việc điều chỉnh có thể được thực hiện qua 2 options sau:
  * **-d:** Tên của 1 trong 2 bộ dataset (oxbuild hoặc paris)
  * **-m:** Tên của 1 trong 6 phương pháp trích xuất đặc trưng
* Các dòng lệnh ví dụ dưới đây sẽ được sử dụng dựa trên phương pháp **Xception**.

### 1. Indexing
* Lập chỉ mục cho bộ dataset Oxford Buildings với câu lệnh dưới đây.
  ```bash
  python systems/indexing.py -d 'oxbuild' -m 'Xception'
  ```

* Lập chỉ mục cho bộ dataset Paris Buildings với câu lệnh dưới đây.
  ```bash
  python systems/indexing.py -d 'paris' -m 'Xception'
  ```

### 2. Evaluating
* Đánh giá cho bộ dataset Oxford Buildings với câu lệnh dưới đây.
  ```bash
  python systems/evaluating.py -d 'oxbuild' -m 'Xception'
  ```

* Đánh giá cho bộ dataset Paris Buildings với câu lệnh dưới đây.
  ```bash
  python systems/evaluating.py -d 'paris' -m 'Xception'
  ```

## [CHẠY HỆ THỐNG TRÊN WEB](#top)
* Web được xây dựng bằng **Flask** với phương pháp **Xception**.
* Chạy dòng lệnh dưới đây để bắt đầu khởi chạy hệ thống.
  ```bash
  flask run
  ```
  
## [DEMO VIDEO](#top)
Bạn có thể xem video demo tại [đây](https://drive.google.com/file/d/1PEYzTG8cKyyJ038J5jCRk0WiGjesT2-0/view?usp=sharing).
