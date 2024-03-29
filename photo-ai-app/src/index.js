import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

const fileUpload = document.getElementById('fileUpload');
const preview = document.getElementById('preview');
const uploadBtn = document.getElementById('uploadBtn'); 

uploadBtn.addEventListener('click', function() {

  // Get file
  const file = fileUpload.files[0];  

  // Check if file
  if(file) {

    // Make preview
    const reader = new FileReader();
    reader.onload = function() {
      const img = document.createElement('img');
      img.src = reader.result;
      
      preview.innerHTML = '';
      preview.appendChild(img);
    }

    reader.readAsDataURL(file);

  }

});

const searchBtn = document.getElementById('search');
const resultImg = document.getElementById('result-img');

searchBtn.addEventListener('click', () => {

  // search logic here

  resultImg.src = 'image.jpg';

  resultImg.style.display = 'block';

});

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
