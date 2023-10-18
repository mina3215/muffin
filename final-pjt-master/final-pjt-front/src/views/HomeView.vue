<template>
  <div class="home">
    <BoxOfficeList/>
  </div>
</template>

<script>
import BoxOfficeList from '@/components/BoxOfficeList.vue'

export default {
  name: 'HomeView',
  components: {
    BoxOfficeList,
  },
  mounted(){
    if(this.$store.state.myAccounts.token){
      this.getrecommend()
    }
  },
  methods : {
    getrecommend(){
      this.$store.dispatch('myAccounts/getrecommend')
      },
  }
}

</script>
