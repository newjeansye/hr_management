<template>
  <div id="app">
    <header class="navbar">
      <div class="logo">HR System</div>
      <nav class="nav-links">
        <router-link to="/employee">员工管理</router-link>
        <router-link to="/department">部门管理</router-link>
        <router-link to="/project">项目管理</router-link>
      </nav>
    </header>

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style>
:root {
  --primary-color: #42b983;
  --dark-bg: #2c3e50;
  --light-gray: #f4f7f6;
}

body {
  margin: 0;
  font-family: 'Segoe UI', Roboto, sans-serif;
  background-color: var(--light-gray);
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  height: 64px;
  background-color: var(--dark-bg);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.logo {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 1px;
}

.nav-links a {
  color: #bdc3c7;
  text-decoration: none;
  margin-left: 30px;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: white;
}

.nav-links a.router-link-active {
  color: var(--primary-color);
  position: relative;
}

.nav-links a.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -22px;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--primary-color);
}

.content {
  max-width: 1200px;
  margin: 30px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  min-height: calc(100vh - 160px);
}
</style>