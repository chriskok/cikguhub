from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	full_name = forms.CharField(label= "Nama Penuh / Full Name (As per NRIC)", required=True)
	school_level = forms.ChoiceField(label= "Anda mengajar di sekolah jenis? / Which school are you teaching in?", choices = (
		("Sekolah Kebangsaan / National Primary School", "Sekolah Kebangsaan / National Primary School"),
		("Sekolah Menengah Kebangsaan / National Secondary School", "Sekolah Menengah Kebangsaan / National Secondary School"),
		("Saya bukan seorang cikgu / I am not a teacher", "Saya bukan seorang cikgu / I am not a teacher"),
		("Other", "Other"),
	), widget=forms.RadioSelect)
	years_of_experience = forms.ChoiceField(label= "Berapakah tahun anda menjadi pendidik? / How long have you been an educator?", choices = (
		("Kurang daripada 1 tahun / Less than 1 year", "Kurang daripada 1 tahun / Less than 1 year"),
		("1 hingga 5 tahun / 1 to 5 years", "1 hingga 5 tahun / 1 to 5 years"),
		("6 hingga 10 tahun / 6 to 10 years", "6 hingga 10 tahun / 6 to 10 years"),
		("Lebih daripada 10 tahun / More than 10 years", "Lebih daripada 10 tahun / More than 10 years"),
	), widget=forms.RadioSelect)
	role = forms.MultipleChoiceField(label= "Apakah jawatan anda di sekolah? / What is your role in school?", choices = (
		("Guru Akademik Biasa / Academic Teacher", "Guru Akademik Biasa / Academic Teacher"),
		("Ketua Panitia / Panel Head", "Ketua Panitia / Panel Head"),
		("Ketua Bidang / Guru Kanan Matapelajaran", "Ketua Bidang / Guru Kanan Matapelajaran"),
		("Penolong Kanan / Assistant Principal", "Penolong Kanan / Assistant Principal"),
		("Guru Besar, Pengetua / Headmaster, Principal", "Guru Besar, Pengetua / Headmaster, Principal"),
		("Other", "Other"),
	), widget=forms.CheckboxSelectMultiple)
	skill_interests = forms.MultipleChoiceField(label= "Apakah kemahiran yang anda ingin bangunkan? / What are the skills you wish to develop?", choices = (
		("Kemahiran Mengajar / Teaching Skills", "Kemahiran Mengajar / Teaching Skills"),
		("Bimbingan & Pementoran / Coaching & Mentoring", "Bimbingan & Pementoran / Coaching & Mentoring"),
		("Kepimpinan / Leadership", "Kepimpinan / Leadership"),
		("Kemahiran Digital / Digital Skills (contoh: aplikasi Microsoft Word/Excel/PowerPoint dan Google Doc/Sheet/Slide)", "Kemahiran Digital / Digital Skills (e.g. Microsoft Word)"),
		("Kemahiran Multimedia / Multimedia Skills (contoh: pembangunan video)", "Kemahiran Multimedia / Multimedia Skills (e.g. Video Making)"),
	), widget=forms.CheckboxSelectMultiple)

	class Meta:
		model = User
		fields = ("username", "full_name", "email", "password1", "password2", "school_level", "years_of_experience")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	
	# def clean(self):
	# 	cleaned_data = super().clean()
	# 	valid = False
	# 	for key, value in cleaned_data.items():
	# 		if value:
	# 			valid = True
	# 			break
	# 	if not valid:
	# 		raise ValidationError("Please input at least one selection")