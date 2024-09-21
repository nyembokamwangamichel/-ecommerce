
# {% extends "base.html" %}

# {% block content %}
# <h2>Passer une commande</h2>
# <form method="post" action="">
#     {% csrf_token %}
#     {{ form.as_p }}
#     <button type="submit" class="btn btn-primary">Passer la commande</button>
# </form>



# {% extends "shop/base.html" %}

# {% block content %}
# <center>
#             {% for order in orders %}
#             <div>
#                 <div>
#                     <div>
#                         <div>
#                             <h2>{{ order.product.name}}</h2>
#                         </div>
#                         <div>
#                             <img src="{{ order.product.image.url }}" alt="{{ ordrer.product.name }}" style="max-width: 250px;">
#                             <span><p>{{order.quantity}} dans le panier </p></span><br>
#                         </div>
#                         <div>
#                             {% if order.prix_total == 0.0 %}
#                             <span><p>prix total € {{order.product.price}}</p></span><br>
#                             {% else %}
#                                 <span><p>prix total € {{order.prix_total}}</p></span>
#                             {% endif %}
#                         </div> 
#                     </div>
#                 </div>
#             </div>
#             {% endfor %}
#             <a href="{% url 'store:delete_cart' %}">Supprimer le panier</a>

# </center>
    
# {% endblock content %}