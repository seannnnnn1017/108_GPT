

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
    readAndProcessFile();
}

function next_Layer_page(){
    nextLayer();
    nextPage();
    readAndProcessFile();
}

const filePath = "C:/Users/user/Desktop/108_GPT-Demo/多元表現綜整心得.txt";

readAndProcessFile(filePath, (err, AI_questions) => {
    if (err) {
        console.error(err);
        return;
    }

    // Now AI_questions contains an array of lines from the file
    console.log(AI_questions);
});