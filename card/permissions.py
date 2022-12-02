from rest_framework import permissions
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError
from users.models import Bank, User, ConsumerProfile
import jwt
from django.conf import settings
from card.models import Card 
from rest_framework.authentication import get_authorization_header
from card.utils import decrypt

class IsIssuerBank(permissions.BasePermission):


    def has_permission(self, request, view):
        print('IsIssuerBank permission check running...')
        print({"view_dir":dir(view)})
        print(request.GET.get('cardId'))

        headers = get_authorization_header(request)
        print({"headers":headers})
        auth_data = headers.decode('utf-8')
        print(auth_data)
        auth_token = auth_data.split(' ')

        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed("token is not valid")
        
        token = auth_token[1]
        try:

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms='HS256'
                )

            print(payload)
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            print(user)

            if user.role != 'BANK':
                raise exceptions.AuthenticationFailed("User should be a bank")
            
            bank = Bank.objects.get(user=user)
            issuer_id = bank.issuerId
            card = Card.objects.get(cardId=request.GET.get('cardId'))
            decrypted_PAN = decrypt(card.fullPAN)

            print({
                "issuer_id":issuer_id,
                "decrypted_PAN":decrypted_PAN
            })

            if issuer_id == decrypted_PAN[:3]:
                return True
            else:
                raise exceptions.AuthenticationFailed("User is not the issuer bank")

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed("Token is expired, Login again")
        
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed("Token is invalid")

        except User.DoesNotExist as ex:
            raise exceptions.AuthenticationFailed("No such user found")


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        consumer = ConsumerProfile.objects.get(user=request.user)
        return obj.consumer == consumer