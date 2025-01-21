import { app } from "./firebase-config.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
import { ref, getDownloadURL, getStorage } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-storage.js";
// Get a reference to the Firebase authentication service
const auth = getAuth(app);

// Check the initial authentication state
onAuthStateChanged(auth, async (user) => {
    const login = document.getElementById("loginButton");
    const signUp = document.getElementById("sign-up");
    if (user) {
        // User is signed in.
        console.log('User is currently signed in:', user);
        login.style.display = "none";
        signUp.style.display = "none";
        const profile = document.getElementById("profile");
        const profilePicture = document.createElement("img");
        profilePicture.style.height = "100%"
        try {
            // Get a reference to the specific Firebase storage bucket
            const storage = getStorage(app);

            // Construct reference to the profile picture using user's UID
            const storageRef = ref(storage, 'profile_pictures/' + user.uid);

            // Get download URL of the profile picture
            const downloadURL = await getDownloadURL(storageRef);

            // Set the src attribute of the img element to the download URL
            profilePicture.src = downloadURL;

            // Append the img element to the profile div
            profile.appendChild(profilePicture);
            profilePicture.style.display = "block";
            profile.style.display = "block";
        } catch (error) {
            console.error('Error fetching profile picture:', error);
        }
    } else {
        const login = document.getElementById("loginButton");
        login.style.display = "block";
        signUp.style.display = "block";
    }
});

document.addEventListener("DOMContentLoaded", function () {

    document.getElementById('loginButton').addEventListener('click', openLoginPop);
    document.getElementById('closeLoginButton').addEventListener('click', closeLoginPop);
    // On sign up page, if user has account
    document.getElementById('loginSignUp').addEventListener('click', openLoginPop);

    // Event listener for the translucent background (popup overlay)
    document.getElementById('loginPopup').addEventListener('click', function (event) {
        if (event.target === this) {
            closeLoginPop();
        }
    });


    function openLoginPop() {
        document.getElementById('loginPopup').style.display = 'block';
        // Print to console
        console.log('Login button clicked');
    }

    function closeLoginPop() {
        document.getElementById('loginPopup').style.display = 'none';
    }


    const form = document.getElementById('signup-form');

    // Password validation for sign-up form
    form.addEventListener('submit', (e) => {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (password !== confirmPassword) {
            alert("Passwords do not match");
            e.preventDefault(); // Prevent form submitting
        }
    });
});

