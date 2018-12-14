<template>
  <div class="writeArticle">
    <group title="写文章">
      <x-input placeholder="标题" v-model="article_title"></x-input>
      <x-textarea :max="200" name="description" placeholder="正文" v-model="article_body"></x-textarea>
    </group>
    <x-button type="primary" @click.native="addArticle()">发布</x-button>
  </div>
</template>

<script>
  import axios from 'axios'
  import { AJAXURL } from '../define.js'
  let _ = require('lodash');
  import qs from 'qs';
  import { XTextarea, Group, XInput, XButton } from 'vux'
export default {
  components: {
    XTextarea,
    Group,
    XInput,
    XButton
  },
  name: 'writeArticle',
  data () {
    return {
      article_title: '',
      article_body: ''
    }
  },
  mounted: function () {

  },
  methods: {
    addArticle: function () {
      let that = this;
      let article_user = sessionStorage.getItem("username");
      let article_userid = sessionStorage.getItem("userid");
      if (that.article_title != ''){
       axios.get(AJAXURL + 'add_article',{
         params: {
           article_title: that.article_title,
           article_body: that.article_body,
           article_user: article_user,
           article_userid: article_userid
         }
       }).then(function (res) {
         let response = res.data;
         if (response.error_num == 0){
           that.$router.go(-1);//跳转写文章页面
           that.input_title = '';
           that.input_body = '';
         }else {
           that.$toast.center('发布失败，请重试')
           console.log(response['msg'])
         }
       })
    }else {
        alert('标题不能为空')
      }
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
