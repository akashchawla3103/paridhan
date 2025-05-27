// Initialize Supabase client
    const supabaseUrl = 'https://brlnmbbndeyyrlhnqkeh.supabase.co';
    const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJybG5tYmJuZGV5eXJsaG5xa2VoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMyNzk2MDAsImV4cCI6MjA1ODg1NTYwMH0.MCnTKk5Np69P4QNBE62OFAz2Ishi07lg-NsWZ7XIvnk';
    const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);
    // DOM elements
    const couponForm = document.getElementById('couponForm');
    const phoneInput = document.getElementById('phone');
    const phoneError = document.getElementById('phoneError');
    const couponInput = document.getElementById('coupon');
    const couponError = document.getElementById('couponError');
    const successMessage = document.getElementById('successMessage');
    const submissionCount = document.getElementById('submissionCount');

    // Load submission count on page load
    document.addEventListener('DOMContentLoaded', loadSubmissionCount);

    // recentSubmissionsContainer = document.getElementById('recentSubmissions');

    // Load recent submissions on page load
    document.addEventListener('DOMContentLoaded', loadRecentSubmissions);

    // Form submission handler
    // Social media click tracking
    let instagramClicked = false;
    let facebookClicked = false;
    let youtubeClicked = false;

    const instagramLink = document.getElementById('instagramLink');
    const facebookLink = document.getElementById('facebookLink');
    const youtubeLink = document.getElementById('youtubeLink');
    const submitButton = document.querySelector('button[type="submit"]');

    // Add click event listeners to track clicks
    instagramLink.addEventListener('click', () => {
      instagramClicked = true;
      updateSubmitButtonState();
    });

    facebookLink.addEventListener('click', () => {
      facebookClicked = true;
      updateSubmitButtonState();
    });

    youtubeLink.addEventListener('click', () => {
      youtubeClicked = true;
      updateSubmitButtonState();
    });

    // Function to update submit button state
    function updateSubmitButtonState() {
      if (instagramClicked && facebookClicked && youtubeClicked) {
        submitButton.disabled = false;
        submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
      } else {
        submitButton.disabled = true;
        submitButton.classList.add('opacity-50', 'cursor-not-allowed');
      }
    }

    // Initialize button state on page load
    document.addEventListener('DOMContentLoaded', function() {
      // Disable submit button initially
      submitButton.disabled = true;
      submitButton.classList.add('opacity-50', 'cursor-not-allowed');
      
      // Load submission count
      loadSubmissionCount();
    });

    // Modify the form submission handler to double-check
    couponForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      // Double-check that all social media links have been clicked
      if (!instagramClicked || !facebookClicked || !youtubeClicked) {
        alert('Please click all social media links before submitting.');
        return;
      }
      
      // Reset error messages
      phoneError.classList.add('hidden');
      couponError.classList.add('hidden');
      
      // Get form values
      const name = document.getElementById('name').value.trim();
      const phone = phoneInput.value.trim();
      const couponCode = couponInput.value.trim();
      const socialMediaChecked = document.getElementById('socialMedia').checked;
      
      // Validate phone number (10 digits)
      if (!validatePhoneNumber(phone)) {
          phoneError.classList.remove('hidden');
          return;
      }
      
      // Validate coupon code
      try {
          const isValid = await validateCoupon(couponCode);
          if (!isValid) {
          couponError.classList.remove('hidden');
          return;
          }
          
          // Check if phone number is already used
          const { data: existingSubmission, error: submissionError } = await supabase
          .from('submissions')
          .select('id')
          .eq('phone_number', phone)
          .single();
          
          if (existingSubmission) {
          phoneError.textContent = 'This phone number has already been used';
          phoneError.classList.remove('hidden');
          return;
          }
          
          // Get coupon ID
          const { data: coupon } = await supabase
          .from('coupons')
          .select('id')
          .eq('code', couponCode)
          .single();
          
          // Submit the form data
          const { data, error } = await supabase
          .from('submissions')
          .insert([
              {
              name: name,
              phone_number: phone,
              coupon_id: coupon.id,
              social_media_verified: socialMediaChecked
              }
          ]);
          
          if (error) throw error;
          
          // Mark coupon as used
          await supabase
          .from('coupons')
          .update({ is_used: true })
          .eq('id', coupon.id);
          
          // Show success message and reset form
          // After successful submission, update the count
          successMessage.classList.remove('hidden');
          couponForm.reset();
          
          // Reload submission count
          loadSubmissionCount();
          
          // Hide success message after 5 seconds
          setTimeout(() => {
          successMessage.classList.add('hidden');
          }, 5000);
          
      } catch (error) {
          console.error('Error submitting form:', error);
          couponError.textContent = 'An error occurred. Please try again.';
          couponError.classList.remove('hidden');
      }
      });

    // Validate phone number (10 digits)
    function validatePhoneNumber(phone) {
    const phoneRegex = /^[0-9]{10}$/;
    return phoneRegex.test(phone);
    }

    // Validate coupon code
    async function validateCoupon(code) {
    try {
        const { data, error } = await supabase
        .from('coupons')
        .select('is_used')
        .eq('code', code)
        .single();
        
        if (error || !data) return false;
        return !data.is_used; // Return true if coupon exists and is not used
    } catch (error) {
        console.error('Error validating coupon:', error);
        return false;
    }
    }

    // Load recent submissions
    async function loadRecentSubmissions() {
    try {
        const { data, error } = await supabase
        .from('submissions')
        .select(`
            id,
            name,
            created_at
        `)
        .order('created_at', { ascending: false })
        .limit(10);
        
        if (error) throw error;
        
        if (data.length === 0) {
        recentSubmissionsContainer.innerHTML = '<p class="text-gray-500 text-center py-8">No submissions yet</p>';
        return;
        }
        
        recentSubmissionsContainer.innerHTML = data.map(submission => `
        <div class="p-4 border rounded-md">
            <div class="font-semibold">${submission.name}</div>
            <div class="text-sm text-gray-500">${new Date(submission.created_at).toLocaleDateString()}</div>
        </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading submissions:', error);
        recentSubmissionsContainer.innerHTML = '<p class="text-red-500 text-center py-8">Error loading submissions</p>';
    }
    }

    // Load submission count
    async function loadSubmissionCount() {
    try {
        const { count, error } = await supabase
        .from('submissions')
        .select('id', { count: 'exact', head: true });
        
        if (error) throw error;
        
        submissionCount.textContent = count || 0;
        
    } catch (error) {
        console.error('Error loading submission count:', error);
        submissionCount.textContent = '?';
    }
    }