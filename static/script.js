function validateForm() {
    const email = document.getElementById('email').value;
    const age = document.getElementById('age').value;
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {
        alert('Please enter a valid email address.');
        return false;
    }

    if (age < 18) {
        alert('Age must be greater than 18.');
        return false;
    }

    return true;
}
