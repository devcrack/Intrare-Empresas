# DJANGO REST FRAMEWORK
[Request Django Rest Framework](https://www.django-rest-framework.org/api-guide/requests/)
## About Request
This class extends the standard HttpRequest, so adding for Rest Framework flexible request parsing and request 
authentication.

### Request Parsing 
Request parsing allows you to treat request with JSON data or other media types in the same way that you would normally
deal with a form data.

#### .data
Returns the parsed content of the request body.


### Content negotation
Expose some properties that allow you to determine the result of the content negotiation stage.
This allows you to implement behaviour such as selecting different schemes for different media types.


### Authentication
This provides flexible, PRE-request Authentication, that gives the ability to:
* Use different authentication polices for different parts of your API.
* Support the use of multiple authentication policies.
* Provide both user and token information associated with the incoming request.

### .user
```request.user``` typically returns an instance of ```django.contrib.models.User```.

If the request is unauthenticated the default value of ```request.user``` is an instance of ```django.contrib.models.AnonymousUser```.

### .auth
```request.auth``` returns any additional authentication context.


## About Athentification
Authentication is the mechanism of associating an incoming request with a set identifying credentials,
so in that sense can use those credentials to determine if the request should be permitted.

### Basic Authentication
Basic authentication is just appropriate For TESTING.  
If successfully authenticated, BasicAuthentication provides the following credentials:

* ```request.user``` : will be a Django user instance.
* ```request.auth``` : will be None.

Unauthenticated response that are denied permission will result in an ```HTPP 401 Unauthorized ```
response.  
 
### TokenAuthentication 
This authentication scheme uses a simple token based HTTP authentication scheme. This type
of authentication is appropriate for client-servers setups, such as native desktop and mobile apps.



## Permissions in DJANGO Rest Framework

The permissions in Django Rest Framework are always run at the very start of the view, before any other code is allowed 
to proceed. Permissions checks will typically use the authentication information in the
```reques.user``` and ```reques.auth```  properties to determine if the incoming request should be permitted.
 
 **Basically permissions are used to grant or deny access for different classes of users to different parts of the API.**
 
The simplest permission corresponds to the ```IsAuthenticated``` class in REST framework, this means that would be to 
to allow access to any authenticated user or deny  access to any unauthenticated user.

Another permission is allow read-only access to unauthenticated users. This corresponds to the ```IsAuthenticatedorReadOnly```
class in RestFramework.   

### How permissions are determined
Permissions are always defined as a list of permission classes.
### Object level permissions
Object level permissions are used to determine if a user should be allowed to act on a particular object, wich will
typically be a model instance.

Object level permission are run by views when ```.get_object()``` is called. An ```exceptions.PermissionDenied``` exception
will be raised if the user is not allowed to act on the given object.

#### Limitations of object level permissions

For performance reasons the generic views will not automatically apply object level permissions to each instance in 
a query set when returning objects.

When you are using object level permissions you will want to filter the queryset appropriately, to ensure that user only 
have visibility onto instance that they are permitted to view.  


## API Quick Reference

### AllowAny 
The ```AllowAny``` permission class wil allow unrestricted access.


### IsAuthenticated
The ```IsAuthenticated``` permission class will deny permission to any unauthenticated user.
This is suitable if you want your API to only be accessible to registered users.


### IsAdminUser
The ```IsAdminUser``` permission class will deny to any user, unless  ```user.is_staff``` is ```True``` in which case 
permission will be allowed.

This permission is suitable if you want your API only be accessible to a subset of trusted administrators.


### IsAuthenticatedOrReadOnly
The ```IsAuthenticatedOrReadOnly``` will allow authenticated users to perform any request. Request for unauthorised
users will only be permitted if the request method **is one of the safe** methods; ```GET```, ```HEAD```, ```OPTIONS```.

This permission is suitable if you want to your API allow read permission to anonymous users.

## DjangoModelPermissions
This permissions must only be applied to views that have a ```.queryset``` property set.

* ```POST``` request require the user to have the ```add``` permission model.
* ```PUT``` and ```PATCH``` request require the user to have the ```change``` permission on the model.
* ```DELETE``` request require the user to have the  ```delete``` permission on the model.


## Custom Permissions

Override ```BasePermission``` and implement either, or both, of the following methods:

* ```.has_permissions(self, request, view)```
* ```.has_object_permissions(self, request, view, obj)```

This methods should return ```True``` if the request should be granted access, and ```False``` otherwise.

### Notes
The instance-level ```has_object_permission``` method will only be called if the view-level ```has_permission``` checks
have already passed. Not that  that for instance-level checks to run, the view code should explicitly call 
```.check_object_permission(request, obj)```. If you are using the **generic views** then this will be handled for you 
by default.

Custom permissions will raise a ```PermissionDenied``` exception if the test fail. To change the error message associated
with the exception, implement a message attribute directly on your custom permission. 

```python
from rest_framework import permissions
class CustomAccessPermision(permissions.BasePermission):
    message = 'Add users not allowed'
    
    
    def has_permission(self, request, view):
        ...
```

### Examples
The following is an example of a permission class that checks the incoming requet's IP address against a blacklist, and 
denies the request if the IP has been blacklisted.

```python
from rest_framework import  permissions
class BlackListPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        blacklisted = Blacklist.object.filter(ip_addr=ip_addr).exists()
        return not blacklisted
```

Ass well global permission, that are run against all incoming request, you can also create object-level permissions,
that are only run against operations that affect a particular object instance.

Example:

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object level permission to only allow owners of an object to edit it.
    Assumes the model instance has an owner attribute. 
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
```
**Note** that the generic views will check the appropriate object level permissions, but if you write your own custom 
views, you need call ```self.check_object_permission(request, obj)``` from the view once you have the object instance.
 
## About Views

### APIView 
This provides some handler methods, to handle the http verbs: get, post, put, patch, and delete.

### ViewSet
This is an abstraction over APIView, which provides actions as methods:
- list
- retrieve
- create
- update/partial_update
- destroy

Both can be used with normal django urls.
Because of the conventions established with the actions, the ViewSet has also the ability to be mapped into a router, 
which is really helpful.

Now, both of this Views, have shortcuts, these shortcuts give you a simple implementation ready to be used.

GenericAPIView: for APIView, this gives you shortcuts that map closely to your database models. Adds commonly required behavior for standard list and detail views. Gives you some attributes like, the serializer_class, also gives pagination_class, filter_backend, etc

GenericViewSet: There are many GenericViewSet, the most common being ModelViewSet. They inherit from GenericAPIView and have a full implementation of all of the actions: list, retrieve, destroy, updated, etc. Of course, you can also pick some of them, read the docs.

If you are doing something really simple, with a ModelViewSet should be enough, even redefining and calling super also is enough. For more complex cases, you can go for lower level classes.

### Viewset

Class is simply a type of class-based View, that does not provide any method handlers such as .get() or .post(), 
and instead provides actions such as ```.list()``` and ```.create()```. This type of view is ussually used when you have 
to do simples tasks.


### ```.list()```
Read only, returns multiple resources (http verb: get). Returns a list of dicts.


### ```.retrieve()```
Read only, single resource (http verb: get, but will expect an id). Returns a single dict.


### ```.create()```
Creates a new resource (http verb: **post**).


### ```update/partial_update```
Edits a resource (http verbs: **put/patch**)

### ```.destroy()```
removes a resource (http verb: **delete**)