import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import VueParticles from 'vue-particles'

Vue.config.productionTip = false

Vue.use(VueParticles)

import VMdEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';
VMdEditor.use(githubTheme, {
  Hljs: hljs,
});
Vue.use(VMdEditor);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
