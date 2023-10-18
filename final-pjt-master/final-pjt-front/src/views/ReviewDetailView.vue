<template>
  <div class="ReviewDetailView">
    <div class="review_detail-box container p-5">
      <!-- 게시글 제목 -->
      <div class="row">
        <div class="title row-2">
          <h1>제목: {{ filteredReview.title }}</h1>
          <hr>
          <div class="write_info d-flex justify-content-between">
            <router-link 
              :to="{
                name: 'profile',
                params : {username: Article_username}
              }" style="color: black; text-decoration: none;">
            <p>작성자: {{ Article_username }}</p>
            </router-link>
            <p>작성한 날짜: {{ created_data }}</p>
          </div>
        </div>
      </div>

      <!-- 게시글 내용 -->
      <div class="row-10 ">
        <div class="row-5">
          <p class="content ">{{ filteredReview.content }}</p>

          <div class="btnarea" v-if="isCurrentUser">
            <button class="btn btn-primary mx-1" @click="gotoEditForm">수정하기</button>
            <button class="btn btn-danger" @click="deleteReview">삭제하기</button>
          </div>
        </div>
      </div>
      <p class="p-5"></p>
      <hr>
       <!-- 댓글 영역 -->
       <div class="row-5">
        <!-- 컴포넌트 하나 만들어서 거기로 보내서, 포문 돌리자. -->
        <div class="comment_list">
          
          <h3 class="cococo">댓글</h3> 
          <div v-if="this.$store.state.reviews.review_comments">
          <div class="card" v-for="(comment) in comments" :key="comment.id">
            <div class="card-body">
                  <ReviewComments :comment="comment" />
                </div>
          </div>
        </div>

        </div>
        
      <form @submit.prevent="createComment">
        <textarea id="content" class="form-control no-resize" rows="3" v-model="comments_content"></textarea>
        <button type="submit" class="mt-5 btn btn-primary btn-lg btn-block">댓글작성</button>
        <button type="button" @click="goToReviewBoard" class="mt-5 mx-1 btn btn-primary btn-lg btn-block">돌아가기</button>

      </form>




      </div>
    </div>
  </div>
</template>


<script>
const API_URL = 'http://127.0.0.1:8000/muffins/'
import axios from 'axios'
import ReviewComments from '@/components/ReviewComments'

export default {
  name: 'ReviewDetailView',


  data() {
    return {
      replyContent: '',
      reviewId: null,
      Article_username : '',
      comments_content : "" 

    };
  },
  components:{
    ReviewComments
  },
  mounted() {
    this.reviewId = this.$route.params.reviewId;
    this.getUserName() 
    this.getReviewComments()
  },
  
  methods: {

    //유저네임 변환
    getUserName(){
      const author = this.filteredReview.author

      axios({
        method: 'get',
        url: `${API_URL}accounts/profile/${author}/`,
      })
      .then((res)=>{
        console.log(res.data)
        this.Article_username = res.data.username
      })
      .catch((err)=>{
        console.log(err,'바보')
      })
    },


    // 수정하기 폼으로 이동
    gotoEditForm() {
    this.$router.push({
      name: 'revieweditform',
      params: {
        id : this.$route.params.id,
        reviewId: this.filteredReview.id
        }
      });
    },
    
    // 리뷰 삭제하기
    deleteReview(){
      const reviewId = this.reviewId;
      const movieId = this.$route.params.id;
      axios
        .delete(`${API_URL}movies/${movieId}/reviews/${reviewId}/`, {
          headers: {
            Authorization: `Token ${this.$store.state.myAccounts.token}`
          }
        })
        .then(() => {
          this.goToReviewBoard()
        })
        .catch((err) => {
          console.log(err);
        });

        
    },

    // 리뷰 보드로 이동
    goToReviewBoard() {
      this.$router.push(`/reviewboard/${this.$route.params.id}`)
    },






    //여기서부턴 댓글 영역
    //댓글 불러오는 건 컴포넌트 For문으로 대체
    //댓글 작성하기
    createComment(){
      const content = this.comments_content.trim()
      if (!content) {
        alert('댓글 내용을 입력해주세요.')
        return;
      }
      const reviewId = this.filteredReview.id

      const author = this.$store.state.myAccounts.username
      const data = {
        
        content : content,
        author : author, 
        review : this.filteredReview.id

      };

      console.log(data)
      axios
      .post(`${API_URL}movies/comments/${reviewId}/`,data, {
          headers: {
            Authorization: `Token ${this.$store.state.myAccounts.token}`
          }
        })
        .then(() => {
          this.getReviewComments()
          this.comments_content = ''
          // this.getMovieComments();
        })
        .catch((err) => {
          console.log(err)
        });


    },


    getReviewComments() {
      const reviewId = this.filteredReview.id
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
          console.log(err);
          console.log("리뷰못불러옴")
        });
      }
    },


  },


  computed: {
  


  filteredReview() {
    const targetReviewId = this.reviewId
    const movieReviews = this.$store.state.reviews.movie_reviews
    // 일치하는 리뷰만 필터링하여 반환
    return movieReviews.filter(review => review.id == targetReviewId)[0]
  },
  created_data() {
    const created_at = this.filteredReview.created_at
    return created_at ? created_at.slice(0, 10) : ''
  },
  isCurrentUser() {
    const loggedInUsername = this.$store.state.myAccounts.username
    return this.Article_username === loggedInUsername
  },

  comments() {
      const targetReviewId = this.reviewId
      const ReviewComments = this.$store.state.reviews.review_comments
      return ReviewComments.filter(review => review.review == targetReviewId)
    },
  },

  

}
  
</script>

<style scoped>


.review_detail-box {
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  backdrop-filter: blur(1px);
  -webkit-backdrop-filter: blur(1px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  padding: 20px;
  
}
.cococo{
  font-weight: bold;
}
.comment_list{
  text-align: left;
}
.title {
  margin-bottom: 20px;
}

.write_info {
  margin-top: 10px;
}

.content {
  white-space: pre-wrap;
  word-wrap: break-word;
  text-align: left;
}

.btnarea {
  margin-top: 20px;
}

.comments {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.comments h3 {
  margin: 0;
}



</style>

