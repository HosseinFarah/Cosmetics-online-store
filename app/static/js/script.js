        // Initialize tooltips
        var tooltipTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        (() => {
          'use strict';
      
          // Define regex patterns for validation
          const patterns = {
              email: /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/, // Email pattern
              password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:'",.<>?/])[A-Za-z\d!@#$%^&*()_+\-=\[\]{}|;:'",.<>?/]{8,}$/, // Password pattern: at least 8 chars, one uppercase, one lowercase, one number, one special character
              firstname:/^[a-zåäöA-ZÅÄÖ'\-]+$/,
              lastname:/^[a-zåäöA-ZÅÄÖ'\-]+$/,
              phone:/^[0-9]{7,15}$/,
              address:/^[a-zåäöA-ZÅÄÖ0-9'\- ]+$/,
              city:/^[a-zåäöA-ZÅÄÖ'\-]+$/,
              zip:/^[0-9]{5}$/,
          };
      
          // Apply validation on input fields
          const forms = document.querySelectorAll('.needs-validation');
      
          forms.forEach(form => {
              form.addEventListener('input', event => {
                  const target = event.target;
                  const pattern = patterns[target.name];
      
                  // If there's a regex pattern for the input name, validate it
                  if (pattern) {
                      if (!pattern.test(target.value)) {
                          target.classList.add('is-invalid');
                      } else {
                          target.classList.remove('is-invalid');
                          target.classList.add('is-valid');
                      }
                  }
              });
      
              form.addEventListener('submit', event => {
                  if (!form.checkValidity()) {
                      event.preventDefault();
                      event.stopPropagation();
                  }
                  form.classList.add('was-validated');
              });
          });
      })();


    //  Preview Selected Image 
      const remove_img = (element) => {
        document.querySelector("#" + element).value = "";
        document.querySelector("#previewImage").src = "";
        document.querySelector("#previewDiv").classList.add("d-none");
        document
          .querySelector("#" + element + "~ .previewDiv")
          .classList.add("d-none");
      };
      const previewImage = document.querySelector("#previewImage");
      if (previewImage) {
        const fileInput = document.querySelector("#image");
        const previewDiv = document.querySelector("#previewDiv");
    
        fileInput.addEventListener("change", () => {
          const file = fileInput.files[0];
          //console.log(file);
          const reader = new FileReader();
          reader.addEventListener("load", () => {
            previewImage.src = reader.result;
          });
    
          if (file) {
            previewDiv.classList.remove("d-none");
            reader.readAsDataURL(file);
          }
        });
      }

// get the cities from the server and populate the city select element
      document.addEventListener('DOMContentLoaded', function() {
        fetch('/auth/cities')
            .then(response => response.json())
            .then(data => {
                const citySelect = document.getElementById('city');
                data.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching cities:', error));
    });