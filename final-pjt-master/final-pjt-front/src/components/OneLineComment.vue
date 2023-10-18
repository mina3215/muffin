<template>
  <div class="comments d-flex">
    <div class="comment-content mt-4 text-center">
      "{{ comment.content }}"
    </div>
    <div class="comment-score" >
      작성자: {{ username }} &nbsp;&nbsp;
      <div class="text-warning fw-bold fs-3" v-if="comment.score">★  {{ comment.score }}.0 </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
const API_URL = 'http://127.0.0.1:8000/muffins/';
export default {

  name: 'OneLineComment',
  data(){
    return{
      username : null
    }
  },
  props: {
    comment: Object,
  },

  methods: {
    getUserName(){
      const author = this.comment.author
      axios({
        method: 'get',
        url: `${API_URL}accounts/profile/${author}/`,

      })
      .then((res)=>{
        this.username = res.data.username
        console.log(this.username)
      })
      .catch((err)=>{
        console.log(err,'바보')
      })
    },

  },

  mounted(){
    console.log(this.comment)
    this.getUserName()
  },

};
</script>

<style scoped>
.comment-content{
  margin-left: 50px;
  font-weight: bold;
  font-size: 25px;
}
.comment-score{
  margin-top: 27px;
}
.comments {
  color: black;
  display: flex;
  justify-content: space-between; 
}

.comment-score {
  margin-left: auto; 
}
</style>
