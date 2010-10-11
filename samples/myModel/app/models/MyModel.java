package models;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

import play.data.validation.MaxSize;
import play.data.validation.MinSize;
import play.data.validation.Required;
import play.db.jpa.Model;

@Entity
public class MyModel extends Model
{
	@Required
	@MinSize(1)
	@MaxSize(100)
	@Column(name="text", nullable=false, length=100)
	public String someText;
}