https://docs.djangoproject.com/en/1.6/ref/contrib/messages/

依赖于template上的:

依赖于在view中调用message.add 之类的


from django.contrib import messages

messages.success(request, 'Your profile was updated.') # ignored
messages.warning(request, 'Your account is about to expire.') # recorded


{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}


