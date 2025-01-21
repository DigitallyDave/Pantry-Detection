// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-analytics.js";
import { getStorage } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-storage.js"
import { getDatabase } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-database.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBHlDge-AgXjd6JyFZ5XZpiwF8TLl-jImA",
  authDomain: "rummage-4800d.firebaseapp.com",
  projectId: "rummage-4800d",
  storageBucket: "rummage-4800d.appspot.com",
  messagingSenderId: "5452201690",
  appId: "1:5452201690:web:18efde7328e2e0a3196fe3",
  measurementId: "G-SB277YBTJ3",
  databaseURL: "https://recipes.firebaseio.com"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const storage = getStorage(app);
const db = getDatabase(app);

export {app, analytics, storage, db};
