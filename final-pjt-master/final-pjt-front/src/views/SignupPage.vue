<template>
  <div>
    <img src="@/assets/logo4.png" alt="" class="logo">
  <div class="ProfileView">
    <div class="">
      <h1>회원가입</h1>
    </div>
    <form @submit.prevent="signup" class="fofofo">
      <input class= input-field placeholder="사용할 아이디" type="text" id="username" v-model="username"><br>

      <input class= input-field  placeholder="비밀번호" type="password" id="password1" v-model="password1"><br>

      <input class= input-field  placeholder="비밀번호 확인" type="password" id="password2" v-model="password2"><br>

      <input class="submit-button" type="submit" value="완료">
    </form>
  </div>
  <footer>
    <img src="@/assets/logo3.png" alt="" class="footer_logo">

     Copyright © Muffin Corp. All Rights Reserved.
  </footer>
</div>
</template>

<script>
// @ is an alias to /src
export default {
  name: 'SignupPage',
  data(){
    return {
      username : null,
      password1 : null,
      password2 : null,
    }
  },
  methods : {
    signup(){
      const username = this.username
      const password1 = this.password1
      const password2 = this.password2
      
      const payload = {
        username, password1, password2
      }
      this.$store.dispatch('myAccounts/signup', payload)
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
