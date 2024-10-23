# dagpt

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Phần 1: Thiết lập dự án
1.	Tạo cấu trúc dự án:
	sử dụng Cookie Cutter Data (lệnh ccds) để tạo cấu trúc thư mục tiêu chuẩn cho dự án phân tích dữ liệu, bao gồm các thư mục như data, notebooks, source code, models, giúp tổ chức code gọn gàng.
        pip install cookiecutter-data-science
        ccds
        project name: dagpt
    …
    Một số thư mục và file không cần thiết được xóa bỏ để tối ưu hóa dự án.
2.	Khởi tạo môi trường ảo & cài đặt thư viện:
    Vào bên trong thư mục: cd dagpt
    Sử dụng python -m venv .venv để tạo môi trường ảo, cách ly thư viện của dự án với hệ thống. 
    Kích hoạt môi trường ảo bằng 
-	Thiết lập chính sách thực thi cho PowerShell: 
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
-	Kích hoạt môi trường ảo trong Terminal của VS code: 
        .\.venv\Scripts\Activate.ps1
    Cài đặt các thư viện cần thiết từ file requirements.txt bằng lệnh 
        #python.exe -m pip install --upgrade pip
        pip install -r requirements.txt
Các thư viện bao gồm:
    LangChain: Tạo "agent" kết nối mô hình ngôn ngữ lớn với các nguồn dữ liệu khác.
    Streamlit: Xây dựng giao diện web tương tác.
    Pandas: Xử lý và phân tích dữ liệu dạng bảng.
    Matplotlib & Plotly: Trực quan hóa dữ liệu.
    dotenv: Nạp biến môi trường từ file .env.
    Các thư viện hỗ trợ khác.
3.	Khởi tạo kho lưu trữ Git:
    Khởi tạo Git trong thư mục dự án: git init.
        Get-ChildItem –Force: hiển thị các thư mục ẩn

    Tạo file .gitignore để bỏ qua những file/thư mục không muốn đưa lên GitHub (ví dụ: môi trường ảo, file dữ liệu nhạy cảm).
    Thêm tất cả thay đổi: git add .
    Commit thay đổi đầu tiên: git commit -m "Initial commit".
-	Tạo kêt nối với tài khoản github
        git config --global user.email "you@example.com"
        git config --global user.name "Your Name"
    Tạo kho lưu trữ mới trên GitHub và kết nối với dự án local.
    Đẩy code lên GitHub: git push origin master.
4.	Nếu thay đổi lần sau: 
        git add .
        git commit -m "bala bala…”
        git push origin master

Phần 2: Xây dựng chức năng hỏi đáp với dữ liệu
1.	Thiết lập giao diện Streamlit:
    Sử dụng st.set_page_config() để đặt tiêu đề trang (page_title), biểu tượng (page_icon) và bố cục (layout).
    Sử dụng st.title(), st.header(), st.write() để thêm nội dung văn bản, tiêu đề và thông điệp chào mừng.
2.	Nạp mô hình ngôn ngữ lớn:
    Tạo hàm load_llm(model_name) trong file source/modules/llm.py để nạp mô hình từ GeminiAI/OpenAI.
    Hàm xử lý việc chọn mô hình dựa trên model_name (mặc định là gemini-1.5-pro-002), thiết lập temperature (độ sáng tạo) và max_tokens (giới hạn số lượng token).
    Hàm có thể mở rộng để hỗ trợ các mô hình khác như Gemini, GPT-4, LLaMa, etc.
3.	Cho phép tải lên tệp CSV:
    Sử dụng st.sidebar.file_uploader() để tạo phần tải lên tệp CSV trong thanh sidebar.
    Lưu trữ DataFrame Pandas được đọc từ tệp CSV vào st.session_state để sử dụng trong các phần khác của ứng dụng.
4.	Khởi tạo lịch sử trò chuyện:
    Sử dụng st.session_state để lưu trữ lịch sử trò chuyện dưới dạng list chứa các cặp (query, response).
5.	Tạo "đại lý" LangChain:
    Tạo hàm create_data_analyst(llm, df) để khởi tạo "đại lý" LangChain sử dụng:
    Mô hình ngôn ngữ lớn (llm).
    DataFrame Pandas chứa dữ liệu (df). 
    agent_type="zero-shot-react-description": cho phép "agent" phản hồi trực tiếp dựa trên mô tả.
    allowed_tools=[...]: danh sách các công cụ mà "agent" được phép sử dụng (ví dụ: truy vấn Pandas).
    verbose=True: in thông tin gỡ lỗi ra console.
    return_intermediate_steps=True: trả về các bước xử lý trung gian của "agent" để lấy code Python.
6.	Xử lý truy vấn & hiển thị kết quả:
    Tạo hàm process_query(query, data_analyst) để xử lý truy vấn của người dùng:
    Gọi data_analyst.run(query) để "agent" xử lý truy vấn.
    Lấy kết quả trả về, bao gồm câu trả lời và các bước xử lý trung gian.
    Kiểm tra xem "agent" có tạo ra code Python để vẽ biểu đồ hay không.
    Nếu có, thực thi code để tạo figure và hiển thị lên Streamlit bằng st.plotly_chart().
    Hiển thị câu trả lời và code Python (nếu có) lên Streamlit.
    Lưu trữ query và response vào lịch sử trò chuyện.
7.	Hiển thị lịch sử trò chuyện:
    Tạo hàm display_chat_history(history) để hiển thị lịch sử trò chuyện lên Streamlit.
    Sử dụng vòng lặp để duyệt qua từng cặp (query, response) trong history.
    Hiển thị query và response bằng st.markdown(), định dạng cho dễ đọc.
Phần 3: Xây dựng chức năng trực quan hóa dữ liệu tương tác
1.  Thiết lập trang Streamlit:
    Sử dụng st.set_page_config() để cấu hình trang tương tự phần 2.
2.	Kiểm tra dữ liệu:
    Kiểm tra xem dữ liệu đã được tải lên hay chưa (kiểm tra st.session_state).
    Nếu chưa, hiển thị thông báo yêu cầu người dùng tải lên dữ liệu.
3.	Render Plotly FigureWidgetResampler:
    Sử dụng st.plotly_chart(df.do_explore()) để render DataFrame Pandas dưới dạng biểu đồ tương tác bằng Plotly FigureWidgetResampler.


A short description of the project.

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         scr and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── scr   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes scr a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

