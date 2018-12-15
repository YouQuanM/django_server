<template>
  <div class="index">
    <div class="index-title">
      WELCOME TO LIANGZHI
    </div>
    <div class="index-introduce">
      <div class="introduce-title">
        <p>Meet us!</p>
      </div>
      <div class="introduce-item">
        <div class="introduce-item-name yh">
          LZC_yh
        </div>
        <div class="introduce-item-content">
          founder of LZC_web, owner of liangzhicompany.com, system maintainer of LZC_web, king of LZC_web_admin
        </div>
      </div>
      <div class="introduce-item">
        <div class="introduce-item-name aoi">
          LZC_aoi
        </div>
        <div class="introduce-item-content">
          设计
        </div>
      </div>
      <div class="introduce-item">
        <div class="introduce-item-name allen">
          LZC_allen
        </div>
        <div class="introduce-item-content">
          好像没什么用
        </div>
      </div>
    </div>
    <div class="index-img">
      <img src="../assets/indeximg.jpeg" width="750" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'index',
  data () {
    return {

    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .index-title { font-family: PingFangSC-Medium;  font-size: 40px;  color: #2D2D2D;  text-align: center; }

  .index-introduce { margin: 40px 32px; }

  .introduce-title p { font-family: PingFangSC-Medium;  font-size: 34px; text-align: center; }

  .introduce-item { margin: 40px 0; border-bottom: 1px solid #E4E8E8; }

  .introduce-item .introduce-item-name { margin: 5px 0; font-family: PingFangSC-Regular;  font-size: 30px;  letter-spacing: 0; }

  .introduce-item .introduce-item-content { font-family: PingFangSC-Regular;  font-size: 28px;  color: #666666;  letter-spacing: 0; }

  .yh { color: #2b85e4; }

  .aoi { color: yellow; }

  .allen { color: red; }
</style>
