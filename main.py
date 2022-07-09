from flask import *
from pytube import YouTube
import os
import re
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *
app=Flask(__name__)
app.secret_key="123"
message=""
path=""
video_url=""
@app.route('/sitemap.xml')
def site_map():
	return render_template('sitemap.xml')
@app.route("/help")
def help():
	return render_template("help_us.html")
@app.route("/whatsnew")
def whatsnew():
	return render_template("whatsnew.html")

@app.route("/google0ee7264dd8861fd6.html")
def google_site_verf():
    return render_template("google0ee7264dd8861fd6.html")
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

'''@app.route('/robots.txt')
def noindex():
    r = Response(response="User-Agent: *\nAllow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r'''
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")
@app.route("/trim",methods=['POST'])
def trim():
	global message
	if request.method=="POST":
		try:
			typeOf=request.form["select"]
			fh=request.form["fromh"]
			fm=request.form["fromm"]
			fs=request.form["froms"]
			th=request.form["toh"]
			tm=request.form["tom"]
			ts=request.form["tos"]
			if fh=="":
				fh='0'
			if fm=="":
				fm='0'
			if fs=="":
				fs='0'
			if th=="":
				th='0'
			if tm=="":
				tm='0'
			if ts=="":
				ts='0'
			fh=int(fh)
			fm=int(fm)
			fs=int(fs)
			th=int(th)
			tm=int(tm)
			ts=int(ts)
			if (fh==0 and fm==0 and fs==0) and (th==0 and tm==0 and ts==0):
				message="Alert : Atleast 1 sec Need To be Trimmed!"
				return redirect(url_for("show"))
			f=(fh*60*60)+(fm*60)+(fs)
			t=(int(th*60*60)+(tm*60)+(ts))
		except Exception as e:
			print(str(e))
			message="Alert : Invalid Entry Detected ! Try Again. "
			return redirect(url_for("show"))

		yt = YouTube(session['url'])
		title=yt.title
		if 'title' in session:
			session.pop('title')
		session['title']=title
		check=os.path.isfile("static/"+session['title']+"720p"+".mp4")
		if not check:
			try:
				out_file=yt.streams.filter(res="720p",file_extension='mp4').first().download("static")
			except Exception as e:
				if "None" in str(e):
					return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
				else:
					return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			if 'title' in session:
				session.pop('title')
			session['title']=title
			try:
				os.rename(out_file, "static/"+session['title']+"720p"+".mp4")
			except:
				pass
			global path
			path=str(os.getcwd()+"/static/"+title+"720p"+".mp4")
		else:
			pass
		path=str(os.getcwd()+"/static/"+title+"720p"+".mp4")
		targetname=str(path)+"video-trimmed"+".mp4"
		ffmpeg_extract_subclip(path, float(f), float(t), targetname=targetname)
		if typeOf=="audio":
			import moviepy.editor as mp
			clip = mp.VideoFileClip(targetname)
			audio = clip.audio
			audio.write_audiofile(str(targetname+".mp3"))
			return send_file(str(str(targetname)+".mp3"),as_attachment=True)
		elif typeOf=="video":
			return send_file(targetname,as_attachment=True)
	return redirect(url_for("home"))
@app.route("/aac")
def audioAac():
	yt = YouTube(session['url'])
	title=yt.title
	if 'title' in session:
		session.pop('title')
	session['title']=title
	check=os.path.isfile("static/"+session['title']+"audio-aac"+".aac")
	if not check:
		try:
			out_file=yt.streams.filter(only_audio=True).first().download("static")
		except Exception as e:
			if "None" in str(e):
				return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			else:
				return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
		if 'title' in session:
			session.pop('title')
		session['title']=title
		try:
			os.rename(out_file, "static/"+session['title']+"audio-aac"+".aac")
		except:
			pass
		global path
		path=str(os.getcwd()+"/static/"+title+"audio-aac"+".aac")
		return send_file(path,as_attachment=True)
	else:
		path=str(os.getcwd()+"/static/"+title+"audio-aac"+".aac")
		return send_file(path,as_attachment=True)

@app.route("/wav")
def audioWav():
	yt = YouTube(session['url'])
	title=yt.title
	if 'title' in session:
		session.pop('title')
	session['title']=title
	check=os.path.isfile("static/"+title+"audio-wav"+".wav")
	if not check:
		try:
			out_file=yt.streams.filter(only_audio=True).first().download("static")
		except Exception as e:
			if "None" in str(e):
				return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			else:
				return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
		if 'title' in session:
			session.pop('title')
		session['title']=title
		try:
			os.rename(out_file, "static/"+session['title']+"audio-wav"+".wav")
		except:
			pass
		global path
		path=str(os.getcwd()+"/static/"+title+"audio-wav"+".wav")
		return send_file(path,as_attachment=True)
	else:
		path=str(os.getcwd()+"/static/"+title+"audio-wav"+".wav")
		return send_file(path,as_attachment=True)
@app.route("/wma")
def audioWma():
	yt = YouTube(session['url'])
	title=yt.title
	if 'title' in session:
		session.pop('title')
	session['title']=title
	check=os.path.isfile("static/"+session['title']+"audio-wma"+".wma")
	if not check:
		try:
			out_file=yt.streams.filter(only_audio=True).first().download("static")
		except Exception as e:
			if "None" in str(e):
				return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			else:
				return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
		if 'title' in session:
			session.pop('title')
		session['title']=title
		try:
			os.rename(out_file, "static/"+session['title']+"audio-wma"+".wma")
		except:
			pass
		global path
		path=str(os.getcwd()+"/static/"+title+"audio-wma"+".wma")
		return send_file(path,as_attachment=True)
	else:
		path=str(os.getcwd()+"/static/"+title+"audio-wma"+".wma")
		return send_file(path,as_attachment=True)

@app.route("/m4a")
def audioM4a():
	yt = YouTube(session['url'])
	title=yt.title
	if 'title' in session:
		session.pop('title')
	session['title']=title

	check=os.path.isfile("static/"+title+"audio-m4a"+".m4a")
	if not check:
		try:
			out_file=yt.streams.filter(only_audio=True).first().download("static")
		except Exception as e:
			if "None" in str(e):
				return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			else:
				return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
		if 'title' in session:
			session.pop('title')
		session['title']=title
		try:
			os.rename(out_file, "static/"+session['title']+"audio-m4a"+".m4a")
		except:
			pass
		global path
		path=str(os.getcwd()+"/static/"+title+"audio-m4a"+".m4a")
		return send_file(path,as_attachment=True)
	else:
		path=str(os.getcwd()+"/static/"+title+"audio-m4a"+".m4a")
		return send_file(path,as_attachment=True)
@app.route("/mp3")
def audioMp3():
	yt = YouTube(session['url'])
	title=yt.title
	if 'title' in session:
		session.pop('title')
	session['title']=title
	check=os.path.isfile("static/"+session['title']+"audio-mp3"+".mp3")
	if not check:
		try:
			out_file=yt.streams.filter(only_audio=True).first().download("static")
		except Exception as e:
			if "None" in str(e):
				return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			else:
				return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
		if 'title' in session:
			session.pop('title')
		session['title']=title
		try:
			os.rename(out_file, "static/"+session['title']+"audio-mp3"+".mp3")
		except:
			pass
		global path
		path=str(os.getcwd()+"/static/"+title+"audio-mp3"+".mp3")
		return send_file(path,as_attachment=True)
	else:
		path=str(os.getcwd()+"/static/"+title+"audio-mp3"+".mp3")
		return send_file(path,as_attachment=True)
@app.route("/1080p")
def res1080p():
	yt = YouTube(session['url'])
	title=yt.title
	if 'title' in session:
		session.pop('title')
	session['title']=title
	check=os.path.isfile(str(str(os.getcwd())+"/static/"+title+"1080p-elgran"+".mp4"))
	if not check:
		try:
			out_file=yt.streams.filter(res="720p",file_extension='mp4').first().download("static")
		except Exception as e:
			if "None" in str(e):
				return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			else:
				return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
		if 'title' in session:
			session.pop('title')
		session['title']=title
		try:
			os.rename(out_file, "static/"+session['title']+"1080p"+".mp4")
		except:
			pass
		global path
		path=str(os.getcwd()+"/static/"+title+"1080p"+".mp4")
		return send_file(path,as_attachment=True)
		try:
			path=str(str(os.getcwd())+"/static/"+title+"480p-elgran"+".mp4")
		except:
			pass
	else:
		path=str(os.getcwd()+"/static/"+title+"1080p"+".mp4")
		try:
			path=str(str(os.getcwd())+"/static/"+title+"1080p-elgran"+".mp4")
		except:
			pass
		return send_file(path,as_attachment=True)
@app.route("/720p")
def res720p():
	yt = YouTube(session['url'])
	title=yt.title
	if 'title' in session:
		session.pop('title')
	session['title']=title
	check=os.path.isfile("static/"+session['title']+"720p"+".mp4")
	if not check:
		try:
			out_file=yt.streams.filter(res="720p",file_extension='mp4').first().download("static")
		except Exception as e:
			if "None" in str(e):
				return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			else:
				return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
		if 'title' in session:
			session.pop('title')
		session['title']=title
		try:
			os.rename(out_file, "static/"+session['title']+"720p"+".mp4")
		except:
			pass
	
		global path
		path=str(os.getcwd()+"/static/"+title+"720p"+".mp4")
		return send_file(path,as_attachment=True)
	else:
		path=str(os.getcwd()+"/static/"+title+"720p"+".mp4")
		return send_file(path,as_attachment=True)

@app.route("/480p")
def res480p():
	yt = YouTube(session['url'])
	title=yt.title
	if 'title' in session:
		session.pop('title')
	session['title']=title
	check=os.path.isfile(str(os.getcwd())+"/static/"+title+"480p-elgran"+".mp4")
	if not check:
		try:
			out_file=yt.streams.filter(res="360p",file_extension='mp4').first().download("static")
		except Exception as e:
			if "None" in str(e):
				return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			else:
				return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
		if 'title' in session:
			session.pop('title')
		session['title']=title
		try:
			os.rename(out_file, "static/"+session['title']+"480p"+".mp4")
		except:
			pass

		global path
		path=str(os.getcwd()+"/static/"+title+"480p"+".mp4")
		
		return send_file(path,as_attachment=True)
	else:
		path=str(os.getcwd()+"/static/"+title+"480p"+".mp4")
		try:
			path=str(str(os.getcwd())+"/static/"+title+"480p-elgran"+".mp4")
		except:
			pass
		return send_file(path,as_attachment=True)
@app.route("/360p")
def res360p():
	yt = YouTube(session['url'])
	title=yt.title
	if 'title' in session:
		session.pop('title')
	session['title']=title
	check=os.path.isfile("static/"+session['title']+"360p"+".mp4")
	if not check:
		try:
			out_file=yt.streams.filter(res="360p",file_extension='mp4').first().download("static")
		except Exception as e:
			if "None" in str(e):
				return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			else:
				print(str(e))
				return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
		if 'title' in session:
			session.pop('title')
		session['title']=title
		try:
			os.rename(out_file, "static/"+session['title']+"360p"+".mp4")
		except:
			pass
		global path
		path=str(os.getcwd()+"/static/"+title+"360p"+".mp4")
		return send_file(path,as_attachment=True)
	else:
		path=str(os.getcwd()+"/static/"+title+"360p"+".mp4")
		return send_file(path,as_attachment=True)
@app.route("/144p")
def res144p():
	
	yt = YouTube(session['url'])
	title=yt.title
	if 'title' in session:
		session.pop('title')
	session['title']=title
	check=os.path.isfile("static/"+session['title']+"144p"+".mp4")
	if not check:

		try:
			out_file=yt.streams.filter(res="144p",progressive=True).first().download("static")

		except Exception as e:
			if "None" in str(e):
				return render_template('downloadbelf.html',message="Alert : Resolution Unavailable.Try Next!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
			else:
				return render_template("downloadbelf.html",message="Alert : Unknown Error Occured!",s=video_url,first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])
		try:
			os.rename(out_file, "static/"+session['title']+"144p"+".mp4")
		except:
			pass
		global path
		path=str(os.getcwd()+"/static/"+title+"144p"+".mp4")
		return send_file(path,as_attachment=True)
	else:
		path=str(os.getcwd()+"/static/"+title+"144p"+".mp4")
		return send_file(path,as_attachment=True)


@app.route("/show")
def show():
	try:
		with open('static/viewsonshow.txt','r') as f:
			val=int(f.read())
			f.close()
		val=val+1
		with open('static/viewsonshow.txt','w') as f:
			f.write(str(val))
	except Exception as e:
		print(str(e))
	global video_url
	video_url=session['url']
	if "shorts" in video_url:
		try:
			video_url=video_url.split("/")
			video_url="https://www.youtube.com/embed/"+str(video_url[4])
		except:
			pass
	else:
		try:
		    video_url=session['url']
		    video_url=video_url.split('=')
		    video_url="https://www.youtube.com/embed/"+str(video_url[1])
		except:
		    try:
		        video_url=session['url']
		        video_url=video_url.split('/')
		        video_url="https://www.youtube.com/embed/"+str(video_url[3])
		    except:
		        global message
		        message="An Error Occured With the url!"
		        return render_template("index.html",message=message)
	return render_template("downloadbelf.html",s=video_url,message=message,video_url="Enter Another Url..",first=session['144p_status'],second=session['360p_status'],third=session['480p_status'],fourth=session['720p_status'],fifth=session['1080p_status'])

#validation for instagram #	TO-DO
def validate_url_for_instagram(link):
    instgagram_regex = (
        r'/(?:(?:http|https):\/\/)?(?:www\.)?(?:instagram\.com|instagr\.am)\/([A-Za-z0-9-_\.]+)/im')

    youtube_regex_match = re.match(youtube_regex, link)
    if youtube_regex_match:
        return youtube_regex_match

    return youtube_regex_match

#validation for youtube
def validate_url_for_youtube(link):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, link)
    if youtube_regex_match:
        return youtube_regex_match

    return youtube_regex_match

@app.route("/process",methods=["POST"])
def process():
    
	l = str(request.form["link"])
	check=validate_url_for_youtube(l)
	if l=="":
		return render_template('index.html',message="INVALID URL PROVIDED!")
	elif check!=None:
		if "url" in session:
			session.pop('url')
		session['url']=str(l)
		yt = YouTube(session['url'])
		title=yt.title
		session['144p_status']=""
		session['360p_status']=""
		session['480p_status']=""
		session['720p_status']=""
		session['1080p_status']=""
		ava144p=False
		ava360p=False
		ava480p=False
		ava720p=False
		ava1080p=False
		ava144p1=False
		ava360p1=False
		ava480p1=False
		ava720p1=False
		ava1080p1=False
		for stream in yt.streams.order_by('resolution'):
			if "144p" in str(stream):
					if ("True" in str(stream)) and ("3gpp" in str(stream)):
						session['144p_status']="available"
						ava144p=True
					else:
						if not ava144p: 
							session['144p_status']="video_only"
							ava144p1=True
			if "144p" not in str(stream):
				if not ava144p:
					if not ava144p1:
						session['144p_status']="unavailable"
			if "360p" in str(stream):
					if ("True" in str(stream)) and ("mp4" in str(stream)):
						session['360p_status']="available"
						ava360p=True
					else:
						if not ava360p: 
							session['360p_status']="video_only"	
							ava360p1=True
			if "360p" not in str(stream):
				if not ava144p:
					if not ava360p1:
						session['360p_status']="unavailable"

			if "480p" in str(stream):
					if ("True" in str(stream)) and ("mp4" in str(stream)):
						session['480p_status']="available"
						ava480p=True
					else:
						if not ava480p: 
							session['480p_status']="video_only"
							ava480p1=True
			if "480p" not in str(stream):
				if not ava480p:
					if not ava480p1:
						session['480p_status']="unavailable"
			if "720p" in str(stream):
					if ("True" in str(stream)) and ("mp4" in str(stream)):
						session['720p_status']="available"
						ava720p=True
					else:
						if not ava720p: 
							session['720p_status']="video_only"
							ava720p1=True
			if "720p" not in str(stream):
				if not ava720p1:
					if not ava720p1:
						session['720p_status']="unavailable"
			if "1080p" in str(stream):
					if ("True" in str(stream)) and ("mp4" in str(stream)):
						session['1080p_status']="available"
						ava1080p=True
					else:
						if not ava1080p: 
							session['1080p_status']="video_only"
							ava1080p1=True
			if "1080p" not in str(stream):
				if not ava1080p:
					if not ava1080p1:
						session['1080p_status']="unavailable"
			if (session['1080p_status']=="video_only") or (session['1080p_status']=="available"):
				session['720p_status']="available" 
			if (session['1080p_status']=="video_only"):
				session['1080p_status']="available" 

			if (session['480p_status']=="video_only"):
				session['480p_status']="available" 


		return render_template("loader.html",message="Loading Configuration!")
	else:
		return render_template("index.html",message="INVALID LINK PROVIED!")


@app.route('/loading')
def loading():
	return render_template("loader.html")
@app.route("/")
def home():
	try:
		with open('static/viewsonhome.txt','r') as f:
			val=int(f.read())
			f.close()
		val=val+1
		with open('static/viewsonhome.txt','w') as f:
			f.write(str(val))
	except Exception as e:
		print(str(e))
	global message
	message=""
	return render_template("index.html",message=message)


if __name__=="__main__":
	app.run(debug=True,host="0.0.0.0",threaded=True)