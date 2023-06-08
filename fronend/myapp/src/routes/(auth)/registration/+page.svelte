<script>
    let email = "";
    let login = "";
    let password = "";
    let second_password = "";
    export let result = null;
    async function registration () {

        if (email != "" && password != "" && second_password != "" && login != "") {
            const res = await fetch('https://dataset-io.onrender.com/api/registration', {
			method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                // like application/json or text/xml
            },
			body: JSON.stringify({
                login,
				email,
                password,
                second_password
			})
		})
		
		const json = await res.json()
        result = json['response_code']
    }
    else {
        result = 401
    }
		
	}
</script>


<main>
   <!--Form-->
<div class="wr">
    <div class="wrapper">
        {#if result == 200}
        <div>
            <div class="alert alert-success">Вы успешно зарегистрировались!</div>
        </div>
        {/if}
        {#if result == 400}
        <div>
            <div class="alert alert-danger">Аккаунт с такой почтой уже зарегистрирован!</div>
        </div>
        {/if}
        {#if result == 401}
        <div>
            <div class="alert alert-danger">Заполните все поля!</div>
        </div>
        {/if}

        <h2 class="in">Регистрация</h2>
        <div class="heading-line"></div>
        <form>

            <div class="field login">
                <div class="input-area">
                    <input type="text" bind:value={login} placeholder="Nickname">
                    <i class="icon fa fa-user"></i>
                    <i class="error error-icon fas fa-exclamation-circle"></i>
                </div>
            </div>

            <div class="field email">
                <div class="input-area">
                    <input type="text" bind:value={email} placeholder="Email Address">
                    <i class="icon fa fa-envelope"></i>
                    <i class="error error-icon fas fa-exclamation-circle"></i>
                </div>
            </div>



            <div class="field password">
                <div class="input-area">
                    <input type="password" bind:value={password} placeholder="Password">
                    <i class="icon fa fa-lock"></i>
                    <i class="error error-icon fas fa-exclamation-circle"></i>
                </div>
            </div>
            <div class="field password">
                <div class="input-area">
                    <input type="password" bind:value={second_password} placeholder="Matching Password">
                    <i class="icon fa fa-lock"></i>
                    <i class="error error-icon fas fa-exclamation-circle"></i>
                </div>
            </div>

            <div class="mb-2">
                <button type="submit" class="form-control btn btn-success" style="border-color: #9e8a78; color:aliceblue" on:click={registration}>Зарегистрироваться</button>
            </div>
            <div>
                <span  class="spann">Уже зарегистрированы? <a style="color: #9e8a78" href="/login">Войдите в аккаунт</a></span>
            </div>
        </form>
    </div>
</div>
<!--Form-->
</main>

<style>
    * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.wr {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #acaec2;
    min-height: 100vh;
    background-position: right;
    background-size: cover;
}
.wrapper {
    min-width: 380px;
    padding: 20px 30px 20px 30px;
    background: #fff;
    border-radius: 8px;
    text-align: center;
}

.wrapper header {
    font-size: 35px;
    font-weight: 600;
}

.wrapper form {
    margin: 40px 0;
}

form .field {
    width: 100%;
    margin-bottom: 20px;
}


form .field .input-area {
    height: 50px;
    width: 100%;
    position: relative;
}

form input {
    width: 100%;
    height: 100%;
    outline: none;
    padding: 0 45px;
    font-size: 18px;
    background: none;
    caret-color: black;
    border-radius: 5px;
    border: 1px solid #bfbfbf;
    border-bottom-width: 2px;
    transition: all 0.2s ease;
}

form .field input:focus,
form .field.valid input {
    border-color: black;
}

form .field.shake input,
form .field.error input {
    border-color: #dc3545;
}

.field .input-area i {
    position: absolute;
    top: 50%;
    font-size: 18px;
    pointer-events: none;
    transform: translateY(-50%);
    color:black;
}

.input-area .icon {
    left: 15px;
    color: #bfbfbf;
    transition: color 0.2s ease;
}

.input-area .error-icon {
    right: 15px;
    color: #dc3545;
}

form input:focus~.icon,
form .field.valid .icon {
    color: black;
}

form .field.shake input:focus~.icon,
form .field.error input:focus~.icon {
    color: #bfbfbf;
}

form input::placeholder {
    color: #bfbfbf;
    font-size: 17px;
}

form .field .error-txt {
    color: #dc3545;
    text-align: left;
    margin-top: 5px;
}

form .field .error {
    display: none;
}

form .field.shake .error,
form .field.error .error {
    display: block;
}

form .pass-txt {
    text-align: left;
    margin-top: -10px;
}


form input[type="submit"] {
    height: 50px;
    margin-top: 30px;
    color: #040404;
    padding: 0;
    border: none;
    background: black;
    cursor: pointer;
    border-bottom: 2px solid black;
    transition: all 0.3s linear;
}

form input[type="submit"]:hover {
    background: grey;
}

.btn {
    background-color: black;
    color: white;
    color: #111B27;
}

</style>