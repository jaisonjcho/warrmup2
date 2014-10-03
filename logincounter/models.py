from django.db import models

class User(models.Model):	
	ERR_BAD_CREDENTIALS = -1
	ERR_BAD_PASSWORD = -4
	ERR_BAD_USERNAME = -3
	ERR_USER_EXISTS = -2
	MAX_PASSWORD_LENGTH = 128
	MAX_USERNAME_LENGTH = 128
	SUCCESS = 1
	
	user = models.CharField(max_length=MAX_USERNAME_LENGTH, unique=True)
	password = models.CharField(max_length=MAX_PASSWORD_LENGTH, blank=True)
	login_count = models.IntegerField(default=1)

	@classmethod
	def login(self, data):
		if data.get('user') and data.get('password'):
			try:
				user = User.objects.get(user=data.get('user'))
			except User.DoesNotExist as e:
				return {'errCode': User.ERR_BAD_CREDENTIALS}
				
			if data.get('password') == user.password:
				user.login_count += 1
				user.save()
				return {'errCode': User.SUCCESS, 'count': user.login_count}
			return {'errCode': User.ERR_BAD_CREDENTIALS}
		return {'errCode': User.ERR_BAD_CREDENTIALS}

	@classmethod
	def add(self, data):
		check = User.validate_user(data)
		if(check == User.SUCCESS):
			try:
				user = User.objects.get(user=data.get('user'))
				return {'errCode': User.ERR_USER_EXISTS}
			except User.DoesNotExist as e:
				user = User(user=data.get('user'), password=data.get('password'))
				user.save()
				return {'errCode': User.SUCCESS, 'count': user.login_count}
		return {'errCode': check}
		
	@classmethod
	def validate_user(self, data):
		if data.get('user') and data.get('password') is not None:
			if len(data.get('user')) == 0 or len(data.get('user')) > User.MAX_USERNAME_LENGTH:
				return User.ERR_BAD_USERNAME
			elif len(data.get('password')) > User.MAX_PASSWORD_LENGTH:
				return User.ERR_BAD_PASSWORD
			return User.SUCCESS
		elif data.get('password') is None:
			return User.ERR_BAD_PASSWORD
		return User.ERR_BAD_USERNAME

	@classmethod
	def resetFixture(self):
		User.objects.all().delete()
		return {'errCode': User.SUCCESS}
		
	def __unicode__(self):
		return self.user
