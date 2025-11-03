<template>
<div class="login_container">
  <div class="login_box" style="box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.2)">
    <el-form
      ref="formRef"
      :model="data.form"
      :rules="data.rules"
      @submit.prevent="handleLogin"
    >
      <div style="text-align: center;font-size: 25px; color:#5372ef; font-weight:bold">欢迎登录</div>
      <el-form-item prop="username">
        <el-input v-model="data.form.username" placeholder="请输入用户名" style="width:300px;height:40px" prefix-icon="User"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input show-password v-model="data.form.password" placeholder="请输入密码" style="width:300px;height:40px" prefix-icon="Lock"></el-input>
      </el-form-item>
      <el-form-item>
        <div style="width:100%">
          <el-button
            type="primary"
            style="width: 100%"
            :loading="data.loading"
            @click="handleLogin"
          >
            {{ data.loading ? '登录中...' : '登录' }}
          </el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { ElMessage } from 'element-plus';
import { authAPI } from '@/services/api.ts'; // 根据你的实际路径导入

const formRef = ref();

const data = reactive({
  form: {
    username: '',
    password: ''
  },
  loading: false,
  rules: {
    username: [
      { required: true, message: "请输入用户名", trigger: "blur" },
    ],
    password: [
      { required: true, message: "请输入密码", trigger: "blur" },
    ]
  }
});

const handleLogin = async () => {
  if (!formRef.value) return;
  const valid = await formRef.value.validate().catch(() => false);
  if (!valid) {
    ElMessage.error('请填写完整的登录信息');
    return;
  }

  data.loading = true;

  try {
    const response = await authAPI.login({
      username: data.form.username,
      password: data.form.password
    });
    if (response.data) {
      ElMessage.success('登录成功！');
      console.log('登录响应数据:', response.data);
      location.href='/about'//登录成功跳转到about界面
    }
  } catch (error: any) {
    console.error('登录错误:', error);
    if (error.detail) {
      ElMessage.error(error.detail);
    } else {
      ElMessage.error('登录失败，请检查用户名和密码');
    }
  } finally {
    data.loading = false;
  }
};
const handleKeyPress = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    handleLogin();
  }
};
import { onMounted, onUnmounted } from 'vue';
onMounted(() => {
  document.addEventListener('keypress', handleKeyPress);
});
onUnmounted(() => {
  document.removeEventListener('keypress', handleKeyPress);
});
</script>
<style scoped>
.login_container{
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-image: url("../assets/login_background.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
.login_box{
  width:320px;
  height:400px;
  background-color: #faf8f8;
  padding: 10px;
  display: flex;
}
</style>
