<template>
  <v-container fluid class="cols pa-1"> <div ref="divc"/>
    <v-row class="header flex-shrink-0">
      head
    </v-row>

    <v-row class="mid">
      <v-col cols="3" class="left">
        <v-list v-if="dirs && ( dirs.length > 0 ) ">
          <v-list-item v-for="mdir in dirs" :key="mdir.id" @click="handleClickDir(mdir)" 
              @contextmenu.prevent="showContextMenuD($event, mdir)"
              :class="{ 'bold-text': mdir.id === cur_dir }">
            {{ mdir.name }}
          </v-list-item>
        </v-list>
        <context-menu-dir v-if="contextMenuDVisible" 
        :position="contextMenuDPosition" :selectedDir="selectedDir"
        @delete="handleDeleteD" @add="handleAddD"
       @refresh="handleRefresh" @adde="handleAddE"  />

      </v-col>

      <v-col cols="3" class="cent">
        <v-list v-if="entries && ( entries.length > 0) ">
          <v-list-item v-for="mentry in entries" :key="mentry.id" @click="handleClickEnt(mentry)" 
              @contextmenu.prevent="showContextMenuE($event, mentry)"
              :class="{ 'bold-text': mentry.id === cur_ent }">
            {{ mentry.name }}
          </v-list-item>
        </v-list>
        <context-menu-ent v-if="contextMenuEVisible" 
        :position="contextMenuEPosition" :selectedEnt="selectedEnt"
        @delete="handleDeleteE"
       @refresh="handleRefreshE"/>

      </v-col>

      <v-col cols="6" class="right" > <div ref="divr"/>
        <div v-if="entry && entry.content && ! edit_mode" @dblclick= "handleClickVal()">{{ entry.content }}</div>
        <Editor :content="entry.content" ref="editor" v-if="entry && entry.content && edit_mode" @dblclick= "handleClickVal()"/>
      </v-col>
    </v-row>

    <v-row class="footer flex-shrink-0">
      <div v-if="fstatus">{{ fstatus }}</div>
    </v-row>
  </v-container>

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import axios from 'axios';
import Editor from '/src/views/Editor.vue';
import ContextMenuDir from '/src/views/ContextMenuDir.vue';
import ContextMenuEnt from '/src/views/ContextMenuEnt.vue';

// Reactive state
const fstatus = ref('loading dirs...');

const dirs = ref([]);
const entries = ref([]);
const entry = ref({});
const editor= ref(null);
const cur_dir= ref(-1);
const cur_ent= ref(-1);
const edit_mode= ref(false);

const contextMenuDVisible = ref(false);
const contextMenuDPosition = ref({ x: 0, y: 0 });
const selectedDir = ref(null);

const contextMenuEVisible = ref(false);
const contextMenuEPosition = ref({ x: 0, y: 0 });
const selectedEnt = ref(null);

let hright=1000;

// Fetch directories on mount
onMounted(() => {
  fetchDirs();
  handleResize();
  window.addEventListener('resize', handleResize);
  document.addEventListener('click', hideContextMenuD);
  document.addEventListener('click', hideContextMenuE);
  console.log("notepad mounted")
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  document.removeEventListener('click', hideContextMenuD);
  document.removeEventListener('click', hideContextMenuE);
  console.log("notepad unmounted")
});

// =========================== Dirs from here ==========================

const fetchDirs = async () => {
  dirs.value = [];
  try{
      const response=await axios.get('http://localhost:8000/backend/dirs/');
      console.log(response.data.length," dirs fetched");
      dirs.value = response.data;
      fstatus.value = '';
    } 
    catch(error)
    {
      fstatus.value = "error while loading dirs: " + error;
    };
    cur_dir.value=-1;
    cur_ent.value=-1;
    entries.value=[]; 
}; 

// Handle directory click
const handleClickDir = (dir) => {
  console.log('click on dir ', dir.id);
  cur_dir.value=dir.id;
  fstatus.value = 'loading entries for dir' + dir.name + '...';
  fetchEnts(dir.id);
}

const fetchEnts = async (id) => {
  entries.value = [] ;
  try {
    const response = await axios.get(`http://localhost:8000/backend/entries/${id}/`)
    console.log(response.data.length," items fetched");
    entries.value = response.data;
    fstatus.value = '';
  }
  catch (error) {
    entries.value = [] ;
    fstatus.value = "error while loading entries for dir id " + id + ': ' + error;
  };
  cur_ent.value = -1;
};

const showContextMenuD = (event, dir) => {
  contextMenuDPosition.value = { x: event.clientX, y: event.clientY };
  contextMenuDVisible.value = true;
  contextMenuEVisible.value = false;
  selectedDir.value = dir;
};

const handleDeleteD = () => {
  if (selectedDir.value) {
    delDirectory(selectedDir.value.id);
  }
  contextMenuDVisible.value = false;
  setTimeout(() => { 
  fetchDirs();
  },500); 
};

const handleAddD = (newDir) => {
  addDirectory(newDir);
  contextMenuDVisible.value = false;
  setTimeout(() => { 
  fetchDirs();
  },500); 
};

const handleRefresh= () =>{
  contextMenuDVisible.value = false;
  fetchDirs();
};


const hideContextMenuD = () => {
  contextMenuDVisible.value = false;
};

const addDirectory = async (dirName) => {
  try {
    const response = await axios.post('http://localhost:8000/backend/dirs/', { name: dirName });
    console.log('Directory added:', response.data);
  } catch (error) {
    console.error('Error adding directory:', error);
  }
};

const delDirectory = async (dirId) => {
  try {
    const response = await axios.delete(`http://localhost:8000/backend/dir/${dirId}/`);
    console.log('Directory deleted:', response.data);
  } catch (error) {
    console.error('Error deleting directory:', error);
  }
};



// =========================== Entries from here ==========================

const showContextMenuE = (event, ent) => {
  contextMenuEPosition.value = { x: event.clientX, y: event.clientY };
  contextMenuEVisible.value = true;
  contextMenuDVisible.value = false;
  selectedEnt.value = ent;
};

const handleDeleteE = () => {
  if (selectedEnt.value) {
    delEntry(selectedEnt.value.id);
  }
  contextMenuEVisible.value = false;
  setTimeout(() => { 
  fstatus.value = 'loading entries for dir' + cur_dir.value + '...';
  fetchEnts(cur_dir.value);
  },500); 
};

const delEntry = async (EntId) => {
  try {
    const response = await axios.delete(`http://localhost:8000/backend/entry/${EntId}/`);
    console.log('Entry deleted:', response.data);
  } catch (error) {
    console.error('Error deleting entry:', error);
  }
};

const handleRefreshE= () =>{
  contextMenuEVisible.value = false;
  setTimeout(() => { 
  fstatus.value = 'loading entries for dir' + cur_dir.value + '...';
  fetchEnts(cur_dir.value);
  },500); 
};

const hideContextMenuE = () => {
  contextMenuEVisible.value = false;
};


const handleAddE= (newElem) =>{
  contextMenuDVisible.value = false;
  if (selectedDir.value)
  {
    CreateNote(newElem, selectedDir.value.id);
    cur_dir.value = selectedDir.value.id;
    setTimeout(() => {
      fetchEnts(cur_dir.value);
    }, 500);
  }
} 

const CreateNote = async (eName,idDir) => {
  try {
    const response = await axios.post(`http://localhost:8000/backend/entries/${idDir}/`, { name: eName , dir_ref: idDir, content : "" });
    console.log('New note added:', response.data);
  } catch (error) {
    console.error('Error adding note :', error);
  }
};

const handleClickEnt = async (ent) => {
  console.log('click on ent ', ent.id);
  cur_ent.value=ent.id;
  fstatus.value = 'loading entry ' + ent.name + '...';
  try {
    const response = await axios.get(`http://localhost:8000/backend/entry/${ent.id}/`);
    entry.value = response.data;
    fstatus.value = '';
  } catch (error) {
    entry.value = {};
    fstatus.value = "error while loading entry " + ent.name + ': ' + error;
  }
};

const handleClickVal = async (ent) => {
  console.log('click on val');
   try {
    edit_mode.value=!edit_mode.value;
    await nextTick(); // wait for editor to come up
    console.log('editor is ', editor.value, 'value ',hright);
    editor.value.calculateTextareaRows(hright); // update row number of editor to match right div
  } catch (error) {
    fstatus.value = "error while editing";
  }
};

// =========================== Resizes as vuetify sucks ==========================

const divc = ref(null);
const divr = ref(null);

// Resize if brother windows change
const handleResize = () => {
  if (divc.value && divr.value && divc.value.parentElement && divr.value.parentElement) {
    console.log(divr.value);

    console.log(divr.value.parentElement.offsetHeight);
    divr.value.parentElement.style.height = (divc.value.parentElement.offsetHeight - 64) + 'px';
    hright = divr.value.parentElement.offsetHeight - 40;
    console.log(divr.value.parentElement.offsetHeight);
  } else {
    console.log("divc/r null")
  }
};
</script>


<style scoped>
.cols {
  background-color: beige;
  height: 100vh;
}

.header {
  background-color: rgb(44, 145, 168);
  /*height: 5%;*/
  height: 32px;
}

.mid {
  background-color: rgb(218, 218, 125);
  /*height: 90%;*/
}

.footer {
  background-color: rgb(99, 165, 150);
  /*height: 5%;*/
  height: 32px;
}

.left {
  background-color: rgb(170, 44, 157);
}

.cent {
  background-color: rgb(162, 84, 193);

}

.right {
  background-color: rgb(185, 146, 226);
}

.dir-item {
  cursor: pointer;
  padding: 10px;
  transition: background-color 0.3s;
}

.dir-item:hover {
  background-color: lightgray;
}

.entry-item {
  padding: 10px;
}

.bold-text {
  font-weight: bold;
}


.context-menu {
  position: absolute;
  z-index: 1000;
  background: white;
  border: 1px solid #ccc;
  padding: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>