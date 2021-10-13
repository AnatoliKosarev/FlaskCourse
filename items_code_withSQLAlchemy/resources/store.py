from flask_restful import Resource

from items_code_withSQLAlchemy.models.store import StoreModel


class Store(Resource):
    @staticmethod
    def _store_exists(name):
        try:
            store = StoreModel.find_by_name(name)
        except:
            return {'message': 'An error occurred when searching the store.'}, 500
        return store

    def get(self, name):
        store = self._store_exists(name)
        if store and isinstance(store, StoreModel):
            return store.json()
        else:
            return {'message': f'Store with name \'{name}\' not found'}, 404

    def post(self, name):
        store_exists = self._store_exists(name)
        if store_exists:
            return {'message': f'the store with name \'{name}\' already exists'}, 400
        try:
            store = StoreModel(name)
            store.save_to_db()
        except:
            return {'message': 'An error occurred when saving the store.'}, 500
        return store.json(), 201

    def delete(self, name):
        store = self._store_exists(name)
        if store and isinstance(store, StoreModel):
            try:
                store.delete_from_db()
            except:
                return {'message': 'An error occurred when deleting the store.'}, 500
        return {'message': f'Store with name \'{name}\' deleted successfully.'}, 201


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
