<template>
  <div class="comments mt-3">
    <div class="comment-content" v-if="!editMode">
      
      <p class="fw-bolder text-primary">{{ username }} &nbsp;&nbsp; {{ date }}</p>
   

      <p class="">{{ comment.content }}</p>
    </div>
    
    <div class="comment-content" v-else>
      <textarea v-model="editCommentContent"></textarea>
    </div>
    
    <div class="editarea" v-if="isCurrentUser">
      <div class="edit-buttons">
        <button class="btn btn-primary" v-if="!editMode" @click="toggleEditMode">수정</button>
        <button class="btn btn-primary" v-else @click="saveEditedComment">저장</button>
        <button class="btn btn-danger" @click="deleteComment">삭제</button>
      </div>
    </div>
  </div>
</template>
<script>

//아이디어
// 수정을 누르면, 기존 코멘트.콘텐트는 가려지고,
// 수정 브이모델을 띄운다.
// 브이모델의 벨류값에 기존 코멘트.콘텐트를 넣어준다.
// 수정 모델에서 다시 수정을 누르면 수정되면서(수정하면서 다시 리뷰 불러와준다) 원래 기존 코멘트 콘텐트를 띄운다



import axios from 'axios';
const API_URL = 'http://127.0.0.1:8000/muffins/';
export default {
  name: 'ReviewComments',
  data(){
    return{
      username: null,
      editMode: false,
      editCommentContent: '',
     
    }
  },
  props: {
    comment: Object,
  },

  methods: {
    getUserName(){
      console.log(this.comment)
      const author = this.comment.author
      console.log(author)

      axios({
        method: 'get',
        url: `${API_URL}accounts/profile/${author}/`,

      })
      .then((res)=>{
        console.log(res.data)
        this.username = res.data.username
      })
      .catch((err)=>{
        console.log(err,'바보')
      })
    },

    toggleEditMode() {
      this.editMode = !this.editMode;
      this.editCommentContent = this.comment.content;
    },


    // 댓글 수정
    saveEditedComment() {
      const content = this.editCommentContent;
      
      const author = this.comment.author;
      const commentId = this.comment.id;
      const reviewId = parseInt(this.$route.params.reviewId)

      if (!content) {
        alert('내용을 입력하세요.');
        return;
      }

      const data = {
        content: content,
        author: author,
        id: commentId,
        review : reviewId,
      };
      console.log(data)
      axios
        .put(`${API_URL}movies/commentsedit/${commentId}/${reviewId}/`, data, {
          headers: {
            Authorization: `Token ${this.$store.state.myAccounts.token}`
          }
        })
        .then(() => {
          this.editMode = false;
          this.getReviewComments();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    deleteComment() {
      const commentId = this.comment.id;
      const reviewId = parseInt(this.$route.params.reviewId)

      axios
        .delete(`${API_URL}movies/commentsedit/${commentId}/${reviewId}/`, {
          headers: {
            Authorization: `Token ${this.$store.state.myAccounts.token}`
          }
        })
        .then(() => {
          this.getReviewComments();
        })
        .catch((err) => {
          this.$store.state.reviews.review_comments = []
          console.log(err);
        });
    },

    getReviewComments() {
      const reviewId = this.$route.params.reviewId
      if (reviewId) {
        axios
       .get(`${API_URL}movies/comments/${reviewId}/`, {
          headers: {
            Authorization: `Token ${this.$store.state.myAccounts.token}`
          }
        })
        .then((res) => {
          this.$store.commit('reviews/GET_REVIEWCOMMENTS', res.data);
        })
        .catch((err) => {
          this.$store.state.reviews.review_comments = []
          console.log(err)
        });
      }
    },
  },

  mounted(){
    this.getReviewComments();
    this.getUserName()

  },
  computed:{
    isCurrentUser() {
    const loggedInUsername = this.$store.state.myAccounts.username;
    return this.username === loggedInUsername;

    
  },
  date(){
    const comment_created_at = this.comment.created_at
    return comment_created_at ? comment_created_at.slice(0, 10) : ''
  }
  }
};
</script>

<style scoped>
.comments {
  color: black;
  font-size: 16px;
  display: flex;
  align-items: center; /* Center align vertically */
  /* background: linear-gradient(to bottom, #ffffff00, #ffffff, #00000000); */

}

.editarea {
  display: flex;
  align-items: center; /* Center align vertically */
}

.edit-buttons {
  align-items: center; /* Center align vertically */
}
</style>
