from flask import Flask, render_template, request, redirect, url_for, session, flash
import db


app = Flask(__name__)
