(function() {
	'use strict';

	var tinyslider = function() {
		var el = document.querySelectorAll('.testimonial-slider');

		if (el.length > 0) {
			var slider = tns({
				container: '.testimonial-slider',
				items: 1,
				axis: "horizontal",
				controlsContainer: "#testimonial-nav",
				swipeAngle: false,
				speed: 700,
				nav: true,
				controls: true,
				autoplay: true,
				autoplayHoverPause: true,
				autoplayTimeout: 3500,
				autoplayButtonOutput: false
			});
		}
	};
	tinyslider();

	


	var sitePlusMinus = function() {

		var value,
    		quantity = document.getElementsByClassName('quantity-container');

		function createBindings(quantityContainer) {
	      var quantityAmount = quantityContainer.getElementsByClassName('quantity-amount')[0];
	      var increase = quantityContainer.getElementsByClassName('increase')[0];
	      var decrease = quantityContainer.getElementsByClassName('decrease')[0];
	      increase.addEventListener('click', function (e) { increaseValue(e, quantityAmount); });
	      decrease.addEventListener('click', function (e) { decreaseValue(e, quantityAmount); });
	    }

	    function init() {
	        for (var i = 0; i < quantity.length; i++ ) {
						createBindings(quantity[i]);
	        }
	    };

	    function increaseValue(event, quantityAmount) {
	        value = parseInt(quantityAmount.value, 10);

	        console.log(quantityAmount, quantityAmount.value);

	        value = isNaN(value) ? 0 : value;
	        value++;
	        quantityAmount.value = value;
	    }

	    function decreaseValue(event, quantityAmount) {
	        value = parseInt(quantityAmount.value, 10);

	        value = isNaN(value) ? 0 : value;
	        if (value > 0) value--;

	        quantityAmount.value = value;
	    }
	    
	    init();
		
	};
	sitePlusMinus();


})()

document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab-item');
    const contents = document.querySelectorAll('.tab-content');

    // Show first tab content by default (with safety check)
    if (contents.length > 0) {
        contents[0].classList.add('active');
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Show corresponding content
            const targetId = tab.getAttribute('data-tab');
            const targetElement = targetId ? document.getElementById(targetId) : null;
            if (targetElement) {
                targetElement.classList.add('active');
            }
        });
    });
});

// Site-wide WhatsApp floating button (injected on every page)
document.addEventListener('DOMContentLoaded', function () {
    // Check if already exists to avoid duplicates
    if (document.querySelector('.whatsapp-float') || !document.body) return;

    var phone = '918925883227'; // WhatsApp number without '+' (edit as needed)
    var text = 'Hi Genoasis, I would like to chat.';
    var href = 'https://wa.me/' + phone + '?text=' + encodeURIComponent(text);

    // Inject minimal styles once
    if (!document.getElementById('whatsapp-float-style')) {
        var style = document.createElement('style');
        style.id = 'whatsapp-float-style';
        style.textContent = '\n.whatsapp-float{position:fixed;right:18px;bottom:18px;z-index:10050}\n.whatsapp-float a{display:flex;align-items:center;gap:10px;background:#25D366;color:#fff;padding:12px 16px;border-radius:28px;text-decoration:none;font-weight:600;box-shadow:0 8px 20px rgba(37,211,102,.3);transition:transform .15s ease,filter .15s ease}\n.whatsapp-float a:hover{filter:brightness(.95);transform:translateY(-1px)}\n.whatsapp-float i{font-size:1.25rem}\n@media(max-width:768px){.whatsapp-float a{padding:10px 14px}}';
        document.head.appendChild(style);
    }

    var container = document.createElement('div');
    container.className = 'whatsapp-float';
    var link = document.createElement('a');
    link.id = 'whatsappButtonGlobal';
    link.href = href;
    link.target = '_blank';
    link.rel = 'noopener';
    link.innerHTML = '<i class="fab fa-whatsapp"></i> Chat with Genoasis on Whatsapp';
    container.appendChild(link);
    document.body.appendChild(container);
});