import 'regenerator-runtime/runtime';
import axios from 'axios';

const progressBar = document.querySelector('#progressBar');

const alert = (message, type) => {
  const alertContainer = document.querySelector('#alertContainer');
  alertContainer.innerHTML = `
    <div class="alert alert-${type}">
      ${message}
    </div>
    `;
};

const setProgress = (percentCompleted) => {
  progressBar.style.width = percentCompleted + '%';
  progressBar.setAttribute('aria-valuenow', percentCompleted);
};

const uploadFile = (file) => {
  const apiUrl = 'http://127.0.0.1:8000/store/products/1/images/';

  const formData = new FormData();
  // "image" is the key that our endpoint expects.
  // Look at ProductImageSerializer for details.
  formData.append('image', file);

  // To send binary data (content of a file) we need
  // to set the Content-Type of the request header to
  // multipart/form-data.
  return axios.post(apiUrl, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (progressEvent) => {
      const { loaded, total } = progressEvent;
      const percentCompleted = Math.round((loaded / total) * 100);
      setProgress(percentCompleted);
    },
  });
};

const handleImageSelect = (event) => {
  const button = document.querySelector('#upload');
  button.disabled = event.target.files.length == 0;
};

const handleSubmit = async (event) => {
  event.preventDefault();

  // Show the progress bar
  setProgress(0);
  progressBar.parentElement.classList.remove('d-none');

  try {
    const image = document.querySelector('#image');
    const response = await uploadFile(image.files[0]);
    alert('Image successfully uploaded!', 'success');
  } catch (err) {
    if (err.response) alert(err.response.data.image[0], 'danger');
    else if (err.request) alert('Could not reach the server!', 'danger');
    else alert('An unexpected error occurred!', 'danger');
  }

  // Hide the progress bar
  progressBar.parentElement.classList.add('d-none');
};

const form = document.querySelector('form');
form.addEventListener('submit', handleSubmit);

const image = document.querySelector('#image');
image.addEventListener('change', handleImageSelect);
