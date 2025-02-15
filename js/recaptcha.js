// Function to handle form submissions with reCAPTCHA
async function getRecaptchaToken(action) {
    try {
        const token = await grecaptcha.execute('6LdbbNEqAAAAAICt9O0PGfaTPi4ikCI8gBVaannf', { action });
        return token;
    } catch (error) {
        console.error('reCAPTCHA error:', error);
        return null;
    }
}
