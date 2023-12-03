let toastBox = document.getElementById('toastBox');
let successMesg = '<i class="bx bxs-check-circle"></i>Operation successful';
let errorMsg = '<i class="bx bx-x-circle"></i>Operation failed';

function showToast(msg) {
    let toast = document.createElement('div');
    toast.classList.add('toast');
    toast.innerHTML = msg;
    toastBox.append(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}

async function signup() {
    const username = document.getElementById('signupUsername').value;
    const password = document.getElementById('signupPassword').value;

    // Check if username or password is empty
    if (!username.trim() || !password.trim()) {
        alert('Username and password are required');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/Users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        });

        const data = await response.json();
        console.log(data);

        if (response.ok) {
            showToast(successMesg);
        } else {
            showToast(errorMsg);
        }
    } catch (error) {
        showToast(errorMsg);
    }
}

async function login() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    // Check if username or password is empty
    if (!username.trim() || !password.trim()) {
        alert('Username and password are required');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        });

        const data = await response.json();
        console.log(data);

        if (response.ok) {
            document.getElementById('loginResult').innerText = 'Login successful';
            localStorage.setItem('token', data.access_token);
            loginSuccess();
        } else {
            document.getElementById('loginResult').innerText = 'Login failed';
            loginfailed();
        }
    } catch (error) {
        console.error('An error occurred during login:', error);
        document.getElementById('loginResult').innerText = 'An error occurred during login';
        // Display an alert with the error message
        alert(error.message);
    }
}

function loginSuccess() {
    showToast(successMesg);
}

function loginfailed() {
    showToast(errorMsg);
}
