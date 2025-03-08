from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from api.v1.accounts.serializer import DatasetSerializer, UserRegisterSerializer, WebDetailsSerializer, WebLoginSerializer
from api.v1.models import DatasetUpload, UserMaster
from myproject.messages import FILE_UPLOAD, UNAUTHORIZED, USER_LOGIN, USER_REGISTER
from myproject.response import http_200_response, http_201_response, http_400_response, http_500_response
import pandas as pd
from rest_framework.parsers import FormParser, MultiPartParser
            

### login
class LoginView(ModelViewSet):
    serializer_class = WebLoginSerializer
    http_method_names = ["post"]
    def get_queryset(self):
        return UserMaster.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            serializer = WebLoginSerializer(data=request.data)
            if serializer.is_valid():       
                user=UserMaster.objects.filter(Q(email=email)|Q(username=email)).last()
                remember_me = request.data.get('remember_me',None)
                user.save()
                serializer_data = WebDetailsSerializer(user,context={'remember_me':remember_me,'request':request,'user':user}).data
                return http_200_response(message=USER_LOGIN,data=serializer_data)
            else:
                if list(serializer.errors.keys())[0] != "error":
                    return http_400_response(message=f"{list(serializer.errors.keys())[0]} : {serializer.errors[list(serializer.errors.keys())[0]][0]}")
                else:
                    return http_400_response(message=serializer.errors[list(serializer.errors.keys())[0]][0])
        except Exception as e:
            return http_500_response(error=str(e)) 
        
class UserRegisterView(ModelViewSet):
    permission_classes = (IsAuthenticated,) 
    http_method_names = ['post']
    serializer_class = UserRegisterSerializer
    queryset = UserMaster.objects.all()
 
    def get_serializer_class(self):
        if self.action == "create":
            return UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            if request.user.user_role_id in [1]:
                serializer = self.get_serializer(data=request.data,context={"request":request,})
                serializer.context['request'] = request  
                if serializer.is_valid():
                    serializer.save()  
                    return http_201_response(message=USER_REGISTER)

                if list(serializer.errors.keys())[0] != "error":
                    return http_400_response(message=f"{list(serializer.errors.keys())[0]} : {serializer.errors[list(serializer.errors.keys())[0]][0]}")
                else:
                    return http_400_response(message=serializer.errors[list(serializer.errors.keys())[0]][0])
            else:
                return http_400_response(message=UNAUTHORIZED)    
        except Exception as e:
            return http_500_response(error=str(e))



class uploadFileView(ModelViewSet):
    queryset = DatasetUpload.objects.all()
    http_method_names = ["post"]
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        try:
            if request.user.user_role_id in [1,2]:
                serializer = DatasetSerializer(data=request.data,context={'request':request})
                if serializer.is_valid():   
                    file_instance=serializer.save()    
                    file_path = file_instance.file.path 
                    processed_data = self.process_file(file_path)
                    return http_201_response(message=FILE_UPLOAD,data=processed_data)
                else:
                    if list(serializer.errors.keys())[0] != "error":
                        return http_400_response(message=f"{list(serializer.errors.keys())[0]} : {serializer.errors[list(serializer.errors.keys())[0]][0]}")
                    else:
                        return http_400_response(message=serializer.errors[list(serializer.errors.keys())[0]][0])
            else:
                return http_400_response(message=UNAUTHORIZED)
        except Exception as e:
            return http_500_response(error=str(e))

    def process_file(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.fillna("N/A", inplace=True)
            df.drop_duplicates(inplace=True)
            return df.to_dict(orient="records")
        except Exception as e:
            return {"error": f"Error processing file: {str(e)}"}   