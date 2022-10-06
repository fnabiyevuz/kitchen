from rest_framework.routers import DefaultRouter
from .viewsets import *

router = DefaultRouter()
router.register('users', UsersViewset)
router.register('products', ProductsViewset)
router.register('rooms', RoomsViewset)
router.register('recieve', RecieveViewset)
router.register('recieveitems', RecieveItemsViewset)
router.register('books', BooksViewset)
router.register('booksitem', BooksItemsViewset)
router.register('chiqim', ChiqimViewset)
router.register('busy', BusyViewset)
router.register('busytype', BusytypeViewset)
router.register('saboy', SaboyViewset)
router.register('saboyitem', SaboyItemViewset)
