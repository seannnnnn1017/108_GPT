

// 初始化數字和總頁數
let currentPage = 1;
const totalPages = 10;
// 函數：點擊前一頁按鈕
function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        updatePageNumber();
    }
}

// 函數：點擊下一頁按鈕
function nextPage() {
    if (currentPage < totalPages) {
        currentPage++;
        updatePageNumber();
        }
}
// 函數：更新顯示的頁碼
function updatePageNumber() {
    document.getElementById('pageNumber').innerText = currentPage;
}

// 設定 label 的初始值
var labelElement = document.getElementById('question');
var question_list = ['請說明你執行過的自主學習計畫。', '請說明你高中社團經驗。', '請描述你的高中幹部經驗。', '請說明你有甚麼服務學習經驗。', '請說明你曾經參加過的競賽。', '有甚麼非修課紀錄之成果作品呢?', '描述你在高中期間考取的檢定證照。', '有甚麼其他特殊優良表現嗎?', '上述問答哪一個活動令你收穫最大。', '請用一句話說明你高中參與這些學習歷程對你帶來的收穫與成長。'];
var question_number = 1; // Start from 0 to display the first question
labelElement.textContent = question_list[question_number];
const total_question = 10;

function prevquestion() {
    if (question_number > 0) {
        question_number--;
        question_show(question_list, question_number);
    }
}

function nextquestion() {
    if (question_number < total_question - 1) {
        question_number++;
        question_show(question_list, question_number);
    }
}

function question_show(dataList, index) {
    var labelElement = document.getElementById('question');
    labelElement.innerText = dataList[index];
}

question_show(question_list, question_number);

// script.js

/// 函數：點擊按鈕時複製 input 內容
function copyInputContent() {
    var inputElement = document.getElementById('inputToCopy');
    
    // 檢查 input 元素是否存在並且有值
    if (inputElement && inputElement.value) {
        // 創建選區範圍（Range）
        var range = document.createRange();
        range.selectNode(inputElement);

        // 將選區範圍的內容複製到剪貼板
        window.getSelection().removeAllRanges(); // 清除之前的選區範圍
        window.getSelection().addRange(range); // 添加新的選區範圍
        document.execCommand('copy'); // 複製到剪貼板s

        // 清除選區範圍，避免對其他內容的影響
        window.getSelection().removeAllRanges();

        // 可以顯示一個提示，表示內容已經複製
        alert('Content copied to clipboard!');
    } else {
        alert('Input is empty or not found.');
    }
}


let currentLayer = 1;
    
      function showLayer(layer) {
        for (let i = 1; i <= 10; i++) {
          document.getElementById(`layer${i}`).style.display = i === layer ? 'flex' : 'none';
        }
      }
    
      function prevLayer() {
        if (currentLayer > 1) {
          currentLayer--;
          showLayer(currentLayer);
        }
      }
    
      function nextLayer() {
        if (currentLayer < 10) {
          currentLayer++;
          showLayer(currentLayer);
        }
      }
    
      // 初始顯示第一層
      showLayer(currentLayer);



function prev_Layer_page(){
    prevLayer();
    prevPage();
    prevquestion();
}

function next_Layer_page(){
    nextLayer();
    nextPage();
    nextquestion();
}
