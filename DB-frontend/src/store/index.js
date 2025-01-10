import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import mutations from './mutations';
import actions from './actions';
import getters from './getters';

export default new Vuex.Store({
  state: {
    count: 0,
    _show_platform_frame_: true,
    _alert_: {
      show: 0,
      message: "default message",
      type: "susscss",
    },
    _role_: 0, // 0: 普通用户, 1: 管理员
    _token_: null,
    _app_title_: "航U邦",
    hasParticles: true,
    _user_id_: null,
    myFavorite: false,
    _follows_: 0,
    _favorites_: 0,
    _shares_: 0,
    _missions_: 0,
    _avatar_url_: "https://s2.loli.net/2024/12/08/MeOiLyYdNt7wK5E.png",
  },
  mutations,
  actions,
  getters,
});
