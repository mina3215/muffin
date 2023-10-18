<template>
  <div>
    <img src="@/assets/logo4.png" alt="" class="logo">
  <div class="ProfileView">
    <div class=""></div>
    <form @submit.prevent="login" class="fofofo">
      <input type="text" id="username" v-model="username" class="input-field" placeholder="아이디">
      <input type="password" id="password" v-model="password" class="input-field" placeholder="비밀번호">

      <input type="submit" value="로그인" class="submit-button">
    </form>
    <nav>
      <p>혹시 가입된 아이디가 없으신가요?</p>
      <router-link :to="{ name: 'signuppage' }">회원가입</router-link>
    </nav>
  </div>
  <footer>
    <img src="@/assets/logo3.png" alt="" class="footer_logo">

     Copyright © Muffin Corp. All Rights Reserved.
  </footer>
</div>
</template>
  
<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      username: null,
      password: null,
    }
  },
  methods: {
    login() {
      const username = this.username
      const password = this.password

      const payload = {
        username,
        password
      }
      this.$store.dispatch('myAccounts/login', payload)
    }
  }
}
</script>

<style scoped>
footer{
  margin-top: 90px;
  font-weight: 200;
  color: white;
  text-shadow: 0px 2px 9px black;

}
.logo{
  width: 20%;
  height: 20%;

}
.footer_logo{
  width: 5%;
  height: 5%;

}
.ProfileView {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 500px;
  height: 400px;
  background-color: #f2f2f2;
  margin: 0 auto; /* 중앙 정렬을 위한 스타일 추가 */

}

h1 {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 30px;
  color: #222222;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  font-size: 16px;
  font-weight: bold;
  color: #666666;
  margin-bottom: 10px;
}
.fofofo{
  box-shadow: #222222;
}
.input-field {
  width: 250px;
  height: 40px;
  padding: 5px;
  font-size: 14px;
  border: 1px solid #dddddd;
  border-radius: 4px;
  
}

.submit-button {
  width: 150px;
  height: 40px;
  background-color: #4285f4;
  color: white;
  font-size: 16px;
  font-weight: bold;
  margin-top: 15px;
  margin-bottom: 35px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #3367d6;
}

nav {
  font-size: 14px;
  color: #666666;
  text-align: center;
}

nav a {
  color: #4285f4;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}
</style>
