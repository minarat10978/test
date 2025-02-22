<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>โปรแกรมแปลงบิลและใบกำกับภาษี</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        #output { white-space: pre-wrap; background: #f8f9fa; padding: 10px; border-radius: 5px; min-height: 200px; }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h2 class="text-center">แปลงบิล/ใบกำกับภาษี เป็นข้อความ</h2>
        <div class="mb-3">
            <input type="file" id="fileInput" class="form-control" accept=".pdf,.png,.jpg,.jpeg">
        </div>
        <button class="btn btn-primary" id="uploadBtn">อัปโหลด</button>
        <hr>
        <div id="pageControls" class="d-none">
            <button class="btn btn-secondary" id="prevPage">⬅️ ก่อนหน้า</button>
            <button class="btn btn-secondary" id="nextPage">ถัดไป ➡️</button>
        </div>
        <h4>ข้อความที่แปลง:</h4>
        <textarea id="output" class="p-3 border"></textarea>
        <button class="btn btn-success mt-3 d-none" id="saveBtn">บันทึกข้อมูลลงฐานข้อมูล</button>
    </div>

    <script>
        let pages = [];
        let currentPage = 0;

        $("#uploadBtn").click(function() {
            let file = $("#fileInput")[0].files[0];
            if (!file) {
                alert("กรุณาเลือกไฟล์ก่อน!");
                return;
            }

            let formData = new FormData();
            formData.append("file", file);

            $.ajax({
                url: "http://127.0.0.1:5000/upload",
                type: "POST",
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    pages = response.pages;
                    currentPage = 0;
                    displayPage();
                },
                error: function() {
                    alert("เกิดข้อผิดพลาดในการอัปโหลด");
                }
            });
        });

        function displayPage() {
            if (pages.length > 0) {
                $("#output").text(pages[currentPage]);
                $("#pageControls").removeClass("d-none");
                $("#saveBtn").removeClass("d-none");
            } else {
                $("#output").text("ไม่พบข้อความในไฟล์");
            }
        }

        $("#prevPage").click(function() {
            if (currentPage > 0) {
                currentPage--;
                displayPage();
            }
        });

        $("#nextPage").click(function() {
            if (currentPage < pages.length - 1) {
                currentPage++;
                displayPage();
            }
        });

        $("#saveBtn").click(function() {
            let data = {
                text: pages.join("\n\n"),
                filename: $("#fileInput")[0].files[0].name
            };

            $.ajax({
                url: "http://127.0.0.1:5000/save",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(data),
                success: function() {
                    alert("บันทึกสำเร็จ!");
                },
                error: function() {
                    alert("เกิดข้อผิดพลาดในการบันทึก");
                }
            });
        });
    </script>
</body>
</html>
