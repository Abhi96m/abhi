<template>
  <div class="sbom-view">
    <h2>Organization / Repo List</h2>
    <table>
      <thead>
        <tr>
          <th>Image Org</th>
          <th>Image Repo</th>
          <th>Image Tag</th>
          <th>Last SBOM Date</th>
          <th>Last EOL Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in orgs" :key="index" @click="selectRepo(item)">
          <td>{{ item.org }}</td>
          <td>{{ item.repo }}</td>
          <td>{{ item.tag }}</td>
          <td>{{ item.sbomDate }}</td>
          <td>{{ item.eolDate }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="selectedRepo" class="drilldown-section">
      <h3>Details for: {{ selectedRepo.org }}/{{ selectedRepo.repo }}:{{ selectedRepo.tag }}</h3>

      <div class="tabs">
        <button v-for="tab in tabs" :key="tab" @click="activeTab = tab" :class="{ active: activeTab === tab }">
          {{ tab }}
        </button>
      </div>

      <div v-if="activeTab === 'SBOM View'">
        <h4>SBOM Data</h4>
        <component-table :components="sbomComponents" @infoClicked="showComponentDetail" />
      </div>

      <div v-if="activeTab === 'EOL View'">
        <h4>EOL Data</h4>
        <component-table :components="eolComponents" @infoClicked="showComponentDetail" />
      </div>

      <div v-if="activeTab === 'Vulnerability View'">
        <h4>Vulnerability Data</h4>
        <component-table :components="vulnComponents" @infoClicked="showComponentDetail" />
      </div>
    </div>

    <component-popup
      v-if="selectedComponent"
      :component="selectedComponent"
      @close="selectedComponent = null"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const orgs = [
  { org: 'test-org', repo: 'test-repo', tag: 'stable', sbomDate: '04/22/2025', eolDate: '04/22/2025' }
]

const selectedRepo = ref(null)
const activeTab = ref('SBOM View')
const tabs = ['SBOM View', 'EOL View', 'Vulnerability View']

const sbomComponents = ref([
  { product: 'Debian', version: '12.10', type: 'Package' }
])

const eolComponents = ref([
  { product: 'Ubuntu', version: '20.04', type: 'Package' }
])

const vulnComponents = ref([
  { product: 'OpenSSL', version: '1.1.1', type: 'Library' }
])

const selectedComponent = ref(null)

const selectRepo = (item) => {
  selectedRepo.value = item
  activeTab.value = 'SBOM View'
}

const showComponentDetail = (component) => {
  selectedComponent.value = component
}
</script>

<script>
export default {
  components: {
    ComponentTable: {
      props: ['components'],
      emits: ['infoClicked'],
      template: `
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Version</th>
              <th>Type</th>
              <th>Info</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(component, index) in components" :key="index">
              <td>{{ component.product }}</td>
              <td>{{ component.version }}</td>
              <td>{{ component.type }}</td>
              <td><button @click="$emit('infoClicked', component)">i</button></td>
            </tr>
          </tbody>
        </table>
      `
    },
    ComponentPopup: {
      props: ['component'],
      emits: ['close'],
      template: `
        <div class="popup">
          <div class="popup-content">
            <h4>Component Detail</h4>
            <p><strong>{{ component.product }}:{{ component.version }}</strong> (Type: {{ component.type }})</p>
            <table>
              <thead><tr><th>Name</th><th>Value</th></tr></thead>
              <tbody><tr><td>aquasecurity.trivy:Class</td><td>os-pkgs</td></tr></tbody>
            </table>
            <button @click="$emit('close')">Close</button>
          </div>
        </div>
      `
    }
  }
}
</script>

<style scoped>
.tabs button.active {
  background-color: #007bff;
  color: white;
}
.popup {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.5);
}
.popup-content {
  background: white;
  margin: 10% auto;
  padding: 20px;
  width: 300px;
  border-radius: 8px;
}
</style>