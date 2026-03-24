// database.js - IndexedDB Database Module for Shiro Notes
class ShiroDB {
  constructor(dbName = 'ShiroNotesDB', version = 1) {
    this.dbName = dbName;
    this.version = version;
    this.db = null;
  }

  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = (event) => {
        console.error('Database error:', event.target.error);
        reject('Error opening database');
      };

      request.onsuccess = (event) => {
        this.db = event.target.result;
        resolve('Database initialized');
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('appData')) {
          db.createObjectStore('appData', { keyPath: 'id' });
        }
      };
    });
  }

  async saveData(data) {
    return new Promise((resolve, reject) => {
      if (!this.db) return reject('Database not initialized.');
      const transaction = this.db.transaction(['appData'], 'readwrite');
      const store = transaction.objectStore('appData');
      const request = store.put({ id: 'main', value: data });

      request.onsuccess = () => resolve();
      request.onerror = (event) => {
        console.error('Error saving data:', event.target.error);
        reject('Failed to save data');
      };
    });
  }

  async loadData() {
    return new Promise((resolve, reject) => {
      if (!this.db) return reject('Database not initialized.');
      const transaction = this.db.transaction(['appData'], 'readonly');
      const store = transaction.objectStore('appData');
      const request = store.get('main');

      request.onsuccess = () => {
        resolve(request.result ? request.result.value : null);
      };
      request.onerror = (event) => {
        console.error('Error loading data:', event.target.error);
        reject('Failed to load data');
      };
    });
  }
}

// Make it globally accessible for the app
window.shiroDB = new ShiroDB();
