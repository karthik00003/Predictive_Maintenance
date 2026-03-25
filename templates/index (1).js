window.onload = function () {

    const wrapper = document.querySelector(".form-wrapper");
    const loginBtn = document.getElementById("loginBtn");
    const signupBtn = document.getElementById("signupBtn");

    if (!wrapper || !loginBtn || !signupBtn) {
        console.log("Elements not found ❌");
        return;
    }

    // Show Login
    window.showLogin = function () {
        wrapper.style.transform = "translateX(0%)";
        loginBtn.classList.add("active");
        signupBtn.classList.remove("active");
    };

    // Show Signup
    window.showSignup = function () {
        wrapper.style.transform = "translateX(-50%)";
        signupBtn.classList.add("active");
        loginBtn.classList.remove("active");
    };

    // Default load
    showLogin();
};