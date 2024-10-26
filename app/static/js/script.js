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
              email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, // Simple email regex pattern
              password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:'",.<>?/])[A-Za-z\d!@#$%^&*()_+\-=\[\]{}|;:'",.<>?/]{8,}$/ // Password pattern: at least 8 chars, one uppercase, one lowercase, one number, one special character
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