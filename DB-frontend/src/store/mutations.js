export default {
  setAppTitle(state, title) {
    state._app_title_ = title;
  },
  setFollows(state, follows) {
    state._follows_ = follows;
  },
  setFavorites(state, favorites) {
    state._favorites_ = favorites;
  },
  setShares(state, shares) {
    state._shares_ = shares;
  },
  setMissions(state, missions) {
    state._missions_ = missions;
  },
  setAvatar(state, avatar) {
    state._avatar_url_ = avatar;
  },
  // 注销账户
  clearPersonalInfo(state) {
    state._user_name_ = null;
    state._token_ = null;
    localStorage.removeItem('__user_name__');
    localStorage.removeItem('_user_role_');
    localStorage.removeItem('_user_id_');
    localStorage.removeItem('_user_avatar_');
    document.cookie = 'session=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
  },
  // 设置是否查看我的收藏
  setMyFavorite(state, myFavorite) {
    state.myFavorite = myFavorite;
  },
  // 从 cookie 中获取Token
  getToken(state) {
    let session = document.cookie.split('; ').find(row => row.startsWith('session='));
    if (session) {
      session = session.split('=')[1];
      state._token_ = session;
    } else state._token_ = null;
  },
  // 从本地存储中获取用户名
  getUserName(state) {
    let user_name = localStorage.getItem('__user_name__');
    let user_role = localStorage.getItem('_user_role_');
    let user_id = localStorage.getItem('_user_id_');
    let avatar = localStorage.getItem('_user_avatar_');
    state._user_name_ = user_name;
    state._role_ = user_role;
    state._user_id_ = user_id;
    if (avatar) {
      state._avatar_url_ = avatar;
    }
  },
  // 设置是否显示颗粒
  setParticles(state, payload) {
    state.hasParticles = payload;
  },
  // 显示警告
  setAlert(state, alert) {
    state._alert_.message = alert.message;
    if (alert.type) {
      state._alert_.type = alert.type;
      state._alert_.show = state._alert_.show + 1;
      setTimeout(() => {
        state._alert_.show = state._alert_.show - 1;
      }, 2000);
    } else {
      state._alert_.show = state._alert_.show - 1;
    }
  },
  // 显示导航栏
  showPlatformFrame(state) {
    state._show_platform_frame_ = true;
  },
  // 隐藏导航栏
  hidePlatformFrame(state) {
    state._show_platform_frame_ = false;
  },
};
