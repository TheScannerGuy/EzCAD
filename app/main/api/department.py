from flask_restx import Namespace, Resource, reqparse
from ..models import DepartmentModel
from ..schemas import DepartmentSchema

api = Namespace('department')


@api.route('/all')
class AllDepartments(Resource):
    def get(self):
        departments = DepartmentModel.query.all()
        return DepartmentSchema(many=True).dump(departments)


@api.route('/<int:departmentId>')
@api.response(404, 'Department does not exist')
class DepartmentById(Resource):
    def get(self, departmentId):
        department = DepartmentModel.query.filter_by(id=departmentId).first()
        if department is None:
            return 404
        return DepartmentSchema().dump(department)

