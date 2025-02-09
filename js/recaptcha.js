// Function to handle form submissions with reCAPTCHA
async function getRecaptchaToken(action = 'default') {
    try {
        const token = await grecaptcha.execute('6LdbbNEqAAAAAICt9O0PGfaTPi4ikCI8gBVaannf', {action: action});
        return token;
    } catch (error) {
        console.error('reCAPTCHA error:', error);
        return null;
    }
}

// Add reCAPTCHA token to all forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const token = await getRecaptchaToken('submit');
            if (token) {
                const tokenInput = document.createElement('input');
                tokenInput.type = 'hidden';
                tokenInput.name = 'g-recaptcha-response';
                tokenInput.value = token;
                form.appendChild(tokenInput);
                form.submit();
            }
        });
    });
}); 