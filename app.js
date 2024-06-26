//js client to test simple api server built with python fastapi

const axios = require("axios");
const readline = require("readline");

const baseURL = "http://localhost:8000"; // FastAPI 서버 주소

// 아이템 생성 함수
async function createItem() {
  try {
    const newItem = {
      name: "포도",
      price: 100.99,
    };

    const response = await axios.post(`${baseURL}/items/`, newItem);
    console.log(response.data);
  } catch (error) {
    console.error("Error creating item:", error.response.data);
  }
}

// 아이템 조회 함수
async function readItem(itemId) {
  try {
    const response = await axios.get(`${baseURL}/items/${itemId}`);
    console.log(response.data);
  } catch (error) {
    console.error("Error reading item:", error.response.data);
  }
}

// 아이템 조회 함수
async function readAllItems(itemId) {
  try {
    const response = await axios.get(`${baseURL}/items/`);
    console.log(response.data);
  } catch (error) {
    console.error("Error reading item:", error.response.data);
  }
}

// 아이템 업데이트 함수
async function updateItem(itemId) {
  try {
    const updatedItem = {
      name: "포도할인",
      price: 50.99,
    };

    const response = await axios.put(`${baseURL}/items/${itemId}`, updatedItem);
    console.log(response.data);
  } catch (error) {
    console.error("Error updating item:", error.response.data);
  }
}

// 아이템 삭제 함수
async function deleteItem(itemId) {
  try {
    const response = await axios.delete(`${baseURL}/items/${itemId}`);
    console.log(response.data);
  } catch (error) {
    console.error("Error deleting item:", error.response.data);
  }
}

// 콘솔 메뉴 표시 함수
function showMenu() {
  console.log("=== Console Menu ===");
  console.log("0. Read All Items");
  console.log("1. Create Item");
  console.log("2. Read [n]th Item");
  console.log("3. Update [n]th Item");
  console.log("4. Delete [n]th Item");
  console.log("9. Exit");
  console.log("====================");
}

// 콘솔 입력 인터페이스 설정
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

// 콘솔 메뉴 실행
function runConsoleMenu() {
  showMenu();
  let num = 8; //n번째 하드코딩캆으로 CRUD테스트 해보는 js code 입니다. 유의하세요.
  console.log("Testing On Item ID:", num);

  rl.question("Select an option: ", async function (option) {
    switch (option) {
      case "0":
        console.log("\nRead All Items...");
        await readAllItems(); // 전체 조회
        break;
      case "1":
        console.log("Creating item...");
        await createItem();
        break;
      case "2":
        console.log("\nReading an item...", num);
        await readItem(num); // 조회할 아이템 ID 입력
        break;
      case "3":
        console.log("\nUpdating item...", num);
        await updateItem(num); // 업데이트할 아이템 ID 입력
        break;
      case "4":
        console.log("\nDeleting item...", num);
        await deleteItem(num); // 삭제할 아이템 ID 입력
        break;
      case "9":
        console.log("Exiting...");
        rl.close();
        return;
      default:
        console.log("Invalid option");
    }
    runConsoleMenu(); // 메뉴 다시 표시
  });
}

// 콘솔 메뉴 실행
runConsoleMenu();
