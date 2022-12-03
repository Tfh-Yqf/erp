<style lang="scss">
  /* 注意要写在第一行，同时给style标签加入lang="scss"属性 */
  @import "@/uni_modules/uview-ui/index.scss";
</style>

<script>
  var globalEvent = uni.requireNativePlugin('globalEvent');

	export default {
		onLaunch: function() {
			console.log('App Launch')
      
      globalEvent.addEventListener('onPrintCallback', function(e) {
        console.log(e.key)
        if (e.key == 0) {
          uni.showToast({
            title: '打印成功',
            duration: 2000
          });
        } else if (e.key == 3) {
          uni.showToast({
            title: '缺纸',
            duration: 2000
          });
        }
      });
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/*每个页面公共css */
</style>
