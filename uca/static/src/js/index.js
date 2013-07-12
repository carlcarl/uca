(function($){
	function post()
	{
		l = $('#link').val()
		$.ajax({
			type: 'GET',
			url: '/api/1/', 
			data: {link: l}, 
			dataTyep: 'json',
			success: function(data){
				response = $('#response');
				if(data.err == false)
				{
					linkNode = '<a href="' + data.hashLink + '">' + data.hashLink + '</a>';
					response.html(linkNode);
					response.attr('class', 'show');
				}
				else
				{
					msg = '';
					switch(data.msg)
					{
					case -1:
						msg = 'Unknown http error';
						break;
					case 1:
						msg = 'Empty url';
						break;
					case 2:
						msg = 'Empty protocol';
						break;
					case 3:
						msg = 'Invalid protocol';
						break;
					case 4:
						msg = 'url too short';
						break;
					case 5:
					default:
						msg = 'Invalid url';
						break;
					}
					msg = 'Error: ' + msg + '!';
					response.html(msg);
					response.attr('class', 'show');
				}
				$('#loading').attr('class', '');
			},
			beforeSend: function(){
				$('#response').attr('class', '');
				$('#loading').attr('class', 'show');
			}
		});
		return false; // Avoid to execute the actual submit
	}
	$('#submit-form').submit(post);
})(jQuery);

