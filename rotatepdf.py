from flask import Flask, jsonify, request, Response
from flask_restful import Resource, Api, reqparse
import PyPDF2
# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)
class RotatePdf(Resource):
    post_args = reqparse.RequestParser()
    post_args.add_argument(
        "file_path", type=str, help="File path is Required", required=True)
    post_args.add_argument(
        "angle_of_rotation", type=int, help="Angle of rotation is Required", required=True)
    post_args.add_argument(
        "page_number", type=int, help="Page number is Required", required=True)
    def post(self):
          
        args = self.post_args.parse_args()
        try:
            pdf_in = open(args['file_path'], 'rb')
        except:
            return Response(response="no such file found on given path",status=400)
        if args['angle_of_rotation']%90 != 0:
            return Response(response="rotation angle should be multiple of 90",status=400)
        pdf_reader = PyPDF2.PdfFileReader(pdf_in)
        pdf_writer = PyPDF2.PdfFileWriter()
        number_of_pages = len(pdf_reader.pages)
        page_to_be_rotated = args['page_number']
        if(number_of_pages<page_to_be_rotated):
            return Response(response="given file has less number of pages than given page number",status=400)
        for page_no in range(number_of_pages):
            page = pdf_reader.getPage(page_no)
            if(page_no+1==page_to_be_rotated):
                page.rotateClockwise(args['angle_of_rotation'])
            pdf_writer.addPage(page)
        pdf_out = open('tmp/rotated.pdf', 'wb')
        pdf_writer.write(pdf_out)
        pdf_out.close()
        pdf_in.close()
        return Response(status=200)
  
  
# adding the defined resources along with their corresponding urls
api.add_resource(RotatePdf, '/rotatepdf')
  
  
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)