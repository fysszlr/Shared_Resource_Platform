import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store';

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/home/'
  },
  // 管理员
  {
    path: '/admin/userManage',
    name: 'user-manage',
    component: () => import('../views/Admin/UserManageView.vue'),
    meta: {
      requiresAuthed: true,
      title: '用户管理'
    }
  },
  {
    path: '/admin/newsManage',
    name: 'news-manage',
    component: () => import('../views/Admin/NewsManageView.vue'),
    meta: {
      requiresAuthed: true,
      title: '公告管理'
    }
  },
  {
    path: '/admin/shareManage',
    name: 'share-manage',
    component: () => import('../views/Admin/ShareManageView.vue'),
    meta: {
      requiresAuthed: true,
      title: '分享管理'
    }
  },
  {
    path: '/admin/taskManage',
    name: 'task-manage',
    component: () => import('../views/Admin/TaskManageView.vue'),
    meta: {
      requiresAuthed: true,
      title: '悬赏管理'
    }
  },
  // 普通用户
  {
    path: '/auth',
    name: 'auth',
    component: () => import('../views/Auth/AuthView.vue'),
    meta: {
      requiresNotAuthed: true,
      title: '登录'
    }
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('../views/Home/HomeView.vue'),
    meta: {
      requiresAuth: true,
      title: '首页'
    }
  },
  {
    path: '/resources',
    name: 'resources',
    component: () => import('../views/Resources/ResourcesView.vue'),
    meta: {
      requiresAuth: true,
      title: '共享资源'
    }
  },
  {
    path: '/resources/share',
    name: 'add-resource',
    component: () => import('../views/Resources/Add/ShareResourceView.vue'),
    meta: {
      requiresAuth: true,
      title: '创建共享'
    }
  },
  {
    path: '/resources/own',
    name: 'own-resource',
    component: () => import('../views/Resources/Own/OwnResourceView.vue'),
    meta: {
      requiresAuth: true,
      title: '我发布的共享资源'
    }
  },
  {
    path: '/resources/:id',
    name: 'get-resource',
    component: () => import('../components/Share/SharePost.vue'),
    meta: {
      requiresAuth: true,
      title: '共享资源'
    }
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: () => import('../views/Tasks/TasksView.vue'),
    meta: {
      requiresAuth: true,
      title: '悬赏'
    },
  },
  {
    path: '/tasks/add',
    name: 'add-task',
    component: () => import('../views/Tasks/Add/AddTaskView.vue'),
    meta: {
      requiresAuth: true,
      title: '添加悬赏'
    }
  },
  {
    path: '/tasks/own',
    name: 'own-task',
    component: () => import('../views/Tasks/Own/OwnTaskView.vue'),
    meta: {
      requiresAuth: true,
      title: '我的悬赏'
    }
  },
  {
    path: '/tasks/:id',
    name: 'task-detail',
    component: () => import('../components/Task/TaskDetail.vue'),
    meta: {
      requiresAuth: true,
      title: '任务详情'
    }
  },
  {
    path: '/center',
    redirect: () => `/center/${store.state._user_id_}`
  },
  {
    path: '/center/:id',
    name: 'center-detail',
    component: () => import('../views/Center/CenterView.vue'),
    meta: {
      requiresAuth: true,
      title: '个人中心'
    }
  },
  {
    path: '/follows',
    name: 'follows',
    component: () => import('../components/Center/MyFollow.vue'),
    meta: {
      requiresAuth: true,
      title: '正在关注'
    }
  },
  {
    path: '/favorites',
    name: 'favorites',
    component: () => import('../components/Center/MyFavorite.vue'),
    meta: {
      requiresAuth: true,
      title: '我的收藏'
    }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/About/AboutView.vue'),
    meta: {
      requiresAuth: false,
      title: '关于我们'
    }
  },
  {
    path: '/giveMeMoney',
    name: 'giveMeMoney',
    component: () => import('../components/Home/GiveMeMoney.vue'),
    meta: {
      requiresAuth: false,
      title: '关于我们'
    }
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  store.commit("getToken");
  store.commit("getUserName");
  const name = store.state._user_name_;
  const default_title = '航 U 邦';
  const title = to.meta == null ? "" : to.meta.title + " | ";
  if (name == null) {
    store.commit("clearPersonalInfo")
    store.commit("hidePlatformFrame")
    if (to.matched.some(record => record.meta.requiresAuth)) {
      next('/auth');
    } else {
      document.title = title + default_title;
      next();
    }
  } else {
    store.commit("showPlatformFrame");
    if (to.matched.some(record => record.meta.requiresNotAuthed)) {
      next('/home');
    } else {
      document.title = title + default_title;
      next();
    }
  }
});

export default router
